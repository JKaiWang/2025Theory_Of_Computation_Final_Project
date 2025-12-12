# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_KEY_PATH = os.path.join(BASE_DIR, "API.txt")

def get_api_key():
    api_key = os.getenv("LLM_API_KEY")
    if api_key:
        return api_key.strip()
    
    if os.path.exists(API_KEY_PATH):
        with open(API_KEY_PATH, "r", encoding="utf-8") as f:
            return f.read().strip()
            
    raise ValueError("找不到 API Key！請設定環境變數 LLM_API_KEY 或建立 API.txt")

LLM_API_KEY = get_api_key()

BASE_URL = "https://api-gateway.netdb.csie.ncku.edu.tw"
MODEL_NAME = "gpt-oss:120b"            

HEADERS = {
    "Authorization": f"Bearer {LLM_API_KEY}",
    "Content-Type": "application/json"
}