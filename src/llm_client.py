import requests
from src.config import BASE_URL, MODEL_NAME, HEADERS

def get_completion(messages):
    """
    發送對話給 LLM 並取得回覆
    messages 格式: [{"role": "user", "content": "..."}, ...]
    """
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
        "temperature": 0.7  # 讓回答稍微有一點變化，不要太死板
    }

    try:
        response = requests.post(f"{BASE_URL}/api/chat", headers=HEADERS, json=payload)
        response.raise_for_status() # 如果是 4xx/5xx 錯誤會直接報錯
        return response.json()['message']['content']
    except Exception as e:
        print(f"API 連線錯誤: {e}")
        return None