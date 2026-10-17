import json
from pathlib import Path
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.config import settings, ROOT
from backend.database import Base, engine, get_db
from backend.models import User, Prediction
from backend.schemas import UserCreate, UserLogin, UserOut, TokenOut
from backend.security import hash_password, verify_password, create_access_token, decode_access_token
from backend.inference import model_service
Base.metadata.create_all(bind=engine)
app=FastAPI(title="MedVision AI API",version="1.0.0",description="Research prototype API. Not for clinical diagnosis.")
app.add_middleware(CORSMiddleware,allow_origins=["http://127.0.0.1:8000","http://localhost:8000"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
bearer=HTTPBearer(auto_error=False); ALLOWED_TYPES={"image/jpeg","image/png","image/webp"}
def current_user(credentials: HTTPAuthorizationCredentials=Depends(bearer),db: Session=Depends(get_db)):
    if not credentials: raise HTTPException(status_code=401,detail="Sign in to continue.")
    subject=decode_access_token(credentials.credentials)
    if not subject: raise HTTPException(status_code=401,detail="Session expired. Please sign in again.")
    user=db.get(User,int(subject))
    if not user: raise HTTPException(status_code=401,detail="Account not found.")
    return user
@app.get("/api/health")
def health(): return {"status":"ok","service":"MedVision AI API"}
@app.get("/api/model/status")
def model_status(): return model_service.status()
@app.post("/api/auth/register",response_model=TokenOut,status_code=201)
def register(payload: UserCreate,db: Session=Depends(get_db)):
    email=payload.email.lower().strip()
    if db.scalar(select(User).where(User.email==email)): raise HTTPException(status_code=409,detail="An account with this email already exists.")
    user=User(full_name=payload.full_name.strip(),email=email,password_hash=hash_password(payload.password)); db.add(user); db.commit(); db.refresh(user)
    return {"access_token":create_access_token(str(user.id)),"user":user}
@app.post("/api/auth/login",response_model=TokenOut)
def login(payload: UserLogin,db: Session=Depends(get_db)):
    user=db.scalar(select(User).where(User.email==payload.email.lower().strip()))
    if not user or not verify_password(payload.password,user.password_hash): raise HTTPException(status_code=401,detail="Incorrect email or password.")
    return {"access_token":create_access_token(str(user.id)),"user":user}
@app.get("/api/auth/me",response_model=UserOut)
def me(user: User=Depends(current_user)): return user
@app.post("/api/predict")
async def predict(file: UploadFile=File(...),user: User=Depends(current_user),db: Session=Depends(get_db)):
    if file.content_type not in ALLOWED_TYPES: raise HTTPException(status_code=415,detail="Upload a PNG, JPEG or WEBP image.")
    content=await file.read(settings.max_upload_mb*1024*1024+1)
    if not content: raise HTTPException(status_code=400,detail="The uploaded file is empty.")
    if len(content)>settings.max_upload_mb*1024*1024: raise HTTPException(status_code=413,detail=f"Maximum upload size is {settings.max_upload_mb} MB.")
    try: result=model_service.predict(content)
    except ValueError as exc: raise HTTPException(status_code=400,detail=str(exc)) from exc
    except RuntimeError as exc: raise HTTPException(status_code=503,detail=str(exc)) from exc
    record=Prediction(user_id=user.id,filename=Path(file.filename or "xray").name[:255],predicted_class=result["predicted_class"],confidence=result["confidence"],probabilities_json=json.dumps(result["probabilities"]))
    db.add(record); db.commit(); db.refresh(record)
    return {"id":record.id,"filename":record.filename,**result,"created_at":record.created_at.isoformat(),"disclaimer":"Research output only; not a diagnosis."}
@app.get("/api/predictions")
def history(user: User=Depends(current_user),db: Session=Depends(get_db)):
    rows=db.scalars(select(Prediction).where(Prediction.user_id==user.id).order_by(Prediction.created_at.desc()).limit(50)).all()
    return [{"id":r.id,"filename":r.filename,"predicted_class":r.predicted_class,"confidence":r.confidence,"probabilities":json.loads(r.probabilities_json),"created_at":r.created_at.isoformat()} for r in rows]
@app.get("/{full_path:path}",include_in_schema=False)
def frontend(full_path: str):
    path=ROOT/"frontend"/"index.html"
    if not path.exists(): raise HTTPException(status_code=404,detail="Frontend file missing.")
    return FileResponse(path)
