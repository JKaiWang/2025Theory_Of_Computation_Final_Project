# web/app.py
import os
import sys
import uuid
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles       # ★★★ 新增
from pydantic import BaseModel
import uvicorn

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(PROJECT_ROOT)

from src.interface.web_agent import WebAgent


app = FastAPI()

# ★★★ 讓 FastAPI 正確 serve web/static/ 裡的檔案
app.mount("/static", StaticFiles(directory=os.path.join(PROJECT_ROOT, "web/static")), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalysisRequest(BaseModel):
    user_name: str
    partner_name: str
    context: str
    chat_logs: str


@app.post("/analyze")
async def analyze(data: AnalysisRequest):
    report = WebAgent.generate_report(
        user_name=data.user_name,
        partner_name=data.partner_name,
        context=data.context,
        chat_logs=data.chat_logs
    )

    if not os.path.exists("web_reports"):
        os.makedirs("web_reports")

    file_id = str(uuid.uuid4())
    filepath = f"web_reports/report_{file_id}.md"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report)

    return {
        "report": report,
        "download_url": f"/download/{file_id}"
    }


@app.get("/download/{file_id}")
async def download(file_id: str):
    filepath = f"web_reports/report_{file_id}.md"

    if not os.path.exists(filepath):
        return JSONResponse({"error": "File not found"}, status_code=404)

    return FileResponse(
        filepath,
        filename=f"analysis_report_{file_id}.md",
        media_type="text/markdown"
    )


@app.get("/")
async def root():
    return FileResponse(os.path.join(PROJECT_ROOT, "web/static/index.html"))


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
