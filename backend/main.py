import os
from typing import Any

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

load_dotenv()

app = FastAPI(title="ReproTrace AI API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BugReport(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=5, max_length=5000)
    error_log: str = Field(default="", max_length=10000)
    language: str = Field(default="Python", max_length=50)

@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "ReproTrace AI API"}

@app.post("/api/analyze")
async def analyze(report: BugReport) -> dict[str, Any]:
    api_key = os.getenv("MODEL_API_KEY", "").strip()
    if not api_key or api_key == "replace_with_your_key":
        raise HTTPException(
            status_code=400,
            detail="Meta API key missing. Add MODEL_API_KEY to backend/.env, then restart the backend.",
        )

    model = os.getenv("META_MODEL", "muse-spark-1.3").strip()
    prompt = f"""You are ReproTrace AI, a cautious software debugging assistant.
Analyze only the evidence provided. Do not claim you ran code or verified a fix.
Clearly label uncertain hypotheses. Return concise, valid JSON with keys:
summary (string), evidence (array of strings), likely_causes (array of objects with
cause, likelihood, reasoning), reproduction_steps (array of strings),
candidate_test (string), confirmation_or_refutation (array of strings), limitations (array of strings).
Bug title: {report.title}
Description: {report.description}
Language: {report.language}
Error log:
{report.error_log or "(not provided)"}
"""

    # Meta API endpoint/model may vary by account; adjust to the endpoint documented for your API access.
    url = os.getenv("META_API_URL", "https://api.meta.ai/v1/chat/completions").strip()
    try:
        async with httpx.AsyncClient(timeout=45) as client:
            response = await client.post(
                url,
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": "Return valid JSON only. Do not invent test results."},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.2,
                },
            )
        if response.is_error:
            detail = response.text[:1200]
            raise HTTPException(status_code=502, detail=f"Meta API returned {response.status_code}: {detail}")
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        return {"status": "analysis_complete", "model": model, "analysis": content, "verified": False}
    except HTTPException:
        raise
    except (httpx.HTTPError, KeyError, IndexError, ValueError) as exc:
        raise HTTPException(status_code=502, detail=f"Could not complete Meta API request: {exc}") from exc
