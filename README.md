## 📄 MedVision AI - Premium README.md (Copy-Paste Ready)

Aap is code ko copy karein aur apne `MedVision_AI_FullStack` folder mein `README.md` file bana kar paste kar dein. Phir `git add .`, `git commit`, aur `git push` kar dein.

---

```markdown
<div align="center">

# 🏥 MedVision AI

### Full-Stack Medical Imaging Research Prototype

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**A responsive premium web frontend, FastAPI backend, SQLite storage, password-hashed user accounts, JWT sessions, DenseNet121 image inference, and saved prediction history.**

[Explore Features](#-features) · [Run Locally](#-run-locally) · [Model Performance](#-model-performance)

</div>

---

## 📸 Interface Preview

*(Yahan aap apne project ke screenshots laga sakte hain. Jab aap screenshots upload karenge, toh in placeholder links ko replace kar dein.)*

<div align="center">
  <img src="https://via.placeholder.com/800x400/1a1a1a/ffffff?text=MedVision+AI+Dashboard" alt="Dashboard Screenshot" style="border-radius: 10px; margin-bottom: 10px;">
</div>

---

## ✨ Key Features

- 🔐 **Secure Authentication** — Password-hashed user accounts with JWT sessions.
- 🧠 **DenseNet121 Inference** — Real four-output model for medical image classification.
- 📊 **Prediction History** — Save and view past predictions per user.
- 🎨 **Premium UI** — Responsive, modern, dark-mode frontend design.
- ⚡ **FastAPI Backend** — High-performance Python API with auto-generated docs.
- 🗄️ **SQLite Storage** — Lightweight, serverless database integration.
- 📈 **Evaluation Plots** — Included in the `artifacts/` directory.

---

## 🛠️ Technology Stack

| Layer | Technologies Used |
|-------|-------------------|
| **Frontend** | HTML5, CSS3, JavaScript, Responsive Design |
| **Backend** | FastAPI, Python 3.10+, Uvicorn |
| **Database** | SQLite (SQLAlchemy ORM) |
| **AI/ML** | PyTorch, DenseNet121, torchvision |
| **Security** | JWT (JSON Web Tokens), Passlib (bcrypt) |

---

## 🚀 Run Locally (Windows)

Follow these steps to run the project on your machine:

**1. Create a virtual environment and activate it:**
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**2. Install dependencies:**
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**3. Setup environment variables:**
```powershell
Copy-Item .env.example .env
```
*(⚠️ Important: Change `SECRET_KEY` in `.env` before deployment)*

**4. Start the server:**
```powershell
uvicorn backend.main:app --reload
```

**5. Open in browser:**
- App: `http://127.0.0.1:8000`
- API Docs: `http://127.0.0.1:8000/docs`

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/model/status` | Check if model is loaded |
| `POST` | `/api/auth/register` | Create new user |
| `POST` | `/api/auth/login` | Login and get JWT token |
| `GET` | `/api/auth/me` | Get current user details |
| `POST` | `/api/predict` | Upload image for prediction (Auth required) |
| `GET` | `/api/predictions` | View past predictions (Auth required) |

---

## 📊 Model Performance

**Confusion Matrix:** 
*(Rows/columns order: COVID19, NORMAL, PNEUMONIA, TB)*

| | COVID19 | NORMAL | PNEUMONIA | TB |
|---|---------|--------|-----------|-----|
| **COVID19** | 101 | 0 | 0 | 5 |
| **NORMAL** | 0 | 196 | 37 | 1 |
| **PNEUMONIA** | 0 | 18 | 372 | 0 |
| **TB** | 0 | 0 | 0 | 41 |

- **Total Samples:** 770
- **Correct Predictions:** 710
- **Overall Accuracy:** **92.2%**

**Model Details:**
- **Architecture:** DenseNet121
- **Input Size:** 224 × 224 RGB
- **Normalization:** ImageNet
- **Output Classes:** COVID19, NORMAL, PNEUMONIA, TB

---

## ⚠️ Medical Safety Notice

> **This is a research/education prototype, not a diagnostic tool.**  
> Model output may be incorrect and must not be used for diagnosis, treatment, or health decisions. Class index order and preprocessing must be verified against the training notebook.

---

## 👤 Author

**Sikandar Ali**

[![GitHub](https://img.shields.io/badge/GitHub-sikandarali2344-181717?style=flat&logo=github)](https://github.com/sikandarali2344)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sikandar_Ali-0A66C2?style=flat&logo=linkedin)](https://www.linkedin.com/in/sikandar-ali-marri-a02128338)
[![Portfolio](https://img.shields.io/badge/Portfolio-sikandario.netlify.app-00C7B7?style=flat&logo=netlify)](https://sikandario.netlify.app)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

<div align="center">
  <br>
  <b>⭐ If you found this project useful, please give it a star! ⭐</b>
</div>
```