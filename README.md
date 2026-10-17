# MedVision AI — Full-Stack Research Prototype

A responsive premium web frontend, FastAPI backend, SQLite storage, password-hashed user accounts, JWT sessions, DenseNet121 image inference and saved prediction history. Your supplied checkpoint and evaluation plots are included in `artifacts/`.

## Run on Windows
1. Install Python 3.10 or 3.11.
2. Open PowerShell in this folder.
3. Run:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn backend.main:app --reload
```
4. Open `http://127.0.0.1:8000` (API docs: `/docs`).

## Run on macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn backend.main:app --reload
```

Change `SECRET_KEY` in `.env` before deployment. Model class order is configured as `COVID19,NORMAL,PNEUMONIA,TB`; confirm the exact output-index order and preprocessing against the training notebook. The included inference transform uses 224x224 RGB ImageNet normalization, so it must match the training preprocessing for valid results. The checkpoint is a real four-output DenseNet121 state dict.

## API
- `GET /api/health`
- `GET /api/model/status`
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `POST /api/predict` (authenticated image upload)
- `GET /api/predictions` (authenticated history)

## Matrix included
Rows/columns order: COVID19, NORMAL, PNEUMONIA, TB. Matrix rows: `101,0,0,5`; `0,196,37,1`; `0,18,372,0`; `0,0,0,41`. Total=770, diagonal=710, derived accuracy=92.2%.

**Medical safety:** This is a research/education prototype, not a diagnostic tool. Model output may be incorrect and must not be used for diagnosis, treatment, or health decisions. Class index order and preprocessing must be verified against the training notebook.
