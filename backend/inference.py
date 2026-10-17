from pathlib import Path
from threading import Lock
from io import BytesIO
import torch
from torch import nn
from torchvision import models, transforms
from PIL import Image, UnidentifiedImageError
from backend.config import settings
class DenseNetService:
    def __init__(self):
        self.model = None; self.error = None; self.lock = Lock()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.transform = transforms.Compose([transforms.Resize((224,224)), transforms.ToTensor(), transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])])
    def load(self):
        with self.lock:
            if self.model is not None: return True
            path = settings.resolved_model_path
            if not path.exists(): self.error=f"Checkpoint not found: {path}"; return False
            try:
                model=models.densenet121(weights=None); model.classifier=nn.Linear(model.classifier.in_features,len(settings.classes))
                state=torch.load(path,map_location="cpu",weights_only=True)
                if isinstance(state,dict) and "state_dict" in state: state=state["state_dict"]
                if isinstance(state,dict) and state and all(k.startswith("module.") for k in state): state={k.removeprefix("module."):v for k,v in state.items()}
                model.load_state_dict(state,strict=True); model.eval().to(self.device); self.model=model; self.error=None; return True
            except Exception as exc: self.error=f"Could not load checkpoint: {type(exc).__name__}: {exc}"; return False
    def status(self):
        ready=self.load()
        return {"ready":ready,"architecture":"DenseNet121","classes":settings.classes,"device":str(self.device),"checkpoint":Path(settings.model_path).name,"error":self.error}
    def predict(self,image_bytes: bytes):
        if not self.load(): raise RuntimeError(self.error or "Model is not ready")
        try: image=Image.open(BytesIO(image_bytes)).convert("RGB")
        except (UnidentifiedImageError,OSError) as exc: raise ValueError("Uploaded file is not a valid image.") from exc
        tensor=self.transform(image).unsqueeze(0).to(self.device)
        with torch.inference_mode(): probs=torch.softmax(self.model(tensor),dim=1)[0].detach().cpu().tolist()
        if len(probs)!=len(settings.classes): raise RuntimeError("Model output count does not match configured class labels.")
        pairs=sorted(zip(settings.classes,probs),key=lambda x:x[1],reverse=True)
        return {"predicted_class":pairs[0][0],"confidence":float(pairs[0][1]),"probabilities":{k:float(v) for k,v in pairs}}
model_service=DenseNetService()
