# ReproTrace AI — working starter

A small React + Vite frontend and FastAPI backend for an evidence-driven bug investigation demo.

## Requirements
- Python 3.10+
- Node.js 18+
- A Meta Model API key (optional for UI/backend health check; required for real AI analysis)

## 1. Backend (Windows PowerShell)
Open a terminal in this folder:
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```
Edit `backend/.env` and put your key after `MODEL_API_KEY=`. Keep this file private; do not upload it to GitHub.

Start backend:
```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```
Backend health check: http://127.0.0.1:8000/api/health

## 2. Frontend
Open a **second** VS Code terminal at the project root:
```powershell
cd frontend
npm.cmd install
npm.cmd run dev
```
Open the localhost URL Vite prints (usually http://localhost:5173).

## Notes
- The frontend calls the local FastAPI backend.
- The backend asks the Meta Model API for hypotheses. It does not execute code, run tests, or verify fixes yet.
- Never paste your API key into chat or commit `.env`.
