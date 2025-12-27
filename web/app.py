# web/app.py
import os
import sys
import uuid
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(PROJECT_ROOT)

from src.interface.web_agent import WebAgent
from src.agent import ChatAgent


app = FastAPI()

# ===== Chat Sessions =====
chat_sessions = {}

# ===== Static =====
app.mount("/static", StaticFiles(directory=os.path.join(PROJECT_ROOT, "web/static")), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Middleware =====
@app.middleware("http")
async def ensure_utf8_and_no_cache(request, call_next):
    response = await call_next(request)
    try:
        path = request.url.path
        if path.startswith("/static") or path.startswith("/download") or path.startswith("/download_chat"):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"

        ctype = response.headers.get("content-type", "")
        if ctype.startswith("text/") and "charset" not in ctype.lower():
            response.headers["Content-Type"] = f"{ctype}; charset=utf-8"
    except Exception:
        pass
    return response

# ===== Models =====
class AnalysisRequest(BaseModel):
    user_name: str
    partner_name: str
    context: str
    chat_logs: str


class ChatStartResponse(BaseModel):
    session_id: str
    reply: str


class ChatMessageRequest(BaseModel):
    session_id: str
    message: str


class ChatMessageResponse(BaseModel):
    reply: str

# ===== Book Mode =====
@app.post("/analyze")
async def analyze(data: AnalysisRequest):
    report = WebAgent.generate_report(
        user_name=data.user_name,
        partner_name=data.partner_name,
        context=data.context,
        chat_logs=data.chat_logs
    )

    os.makedirs("web_reports", exist_ok=True)
    file_id = str(uuid.uuid4())
    filepath = f"web_reports/report_{file_id}.md"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report)

    return {"report": report, "download_url": f"/download/{file_id}"}


# ===== Save History =====
@app.post("/save_history")
async def save_history(data: AnalysisRequest):
    os.makedirs("chat_sessions", exist_ok=True)
    file_id = str(uuid.uuid4())
    filepath = f"chat_sessions/chat_{file_id}.json"

    payload = {
        "user_name": data.user_name,
        "partner_name": data.partner_name,
        "context": data.context,
        "chat_logs": data.chat_logs,
        "timestamp": datetime.utcnow().isoformat()
    }

    import json
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    return {"file_id": file_id, "download_url": f"/download_chat/{file_id}"}


# ===== Chat Mode =====
@app.post("/chat/start", response_model=ChatStartResponse)
async def chat_start():
    sid = str(uuid.uuid4())
    agent = ChatAgent()
    chat_sessions[sid] = agent
    return {"session_id": sid, "reply": agent.history[-1]["content"]}


@app.post("/chat/message", response_model=ChatMessageResponse)
async def chat_message(data: ChatMessageRequest):
    agent = chat_sessions.get(data.session_id)
    if agent is None:
        return JSONResponse({"error": "invalid session"}, status_code=400)

    reply = agent.reply(data.message)
    return {"reply": reply}


# ===== Downloads =====
@app.get("/download_chat/{file_id}")
async def download_chat(file_id: str):
    filepath = f"chat_sessions/chat_{file_id}.json"
    if not os.path.exists(filepath):
        return JSONResponse({"error": "File not found"}, status_code=404)

    return FileResponse(filepath, filename=f"chat_session_{file_id}.json", media_type="application/json")


@app.get("/download/{file_id}")
async def download(file_id: str):
    filepath = f"web_reports/report_{file_id}.md"
    if not os.path.exists(filepath):
        return JSONResponse({"error": "File not found"}, status_code=404)

    return FileResponse(filepath, filename=f"analysis_report_{file_id}.md", media_type="text/markdown")


# ===== Root =====
@app.get("/")
async def root():
    return FileResponse(os.path.join(PROJECT_ROOT, "web/static/index.html"))


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
