import requests
import json

# --- 設定區 ---
# 這是你截圖中的網址 (Base URL)
BASE_URL = "https://api-gateway.netdb.csie.ncku.edu.tw"
# 這是你提供的 API Key
API_KEY = "83a2443ff6bc54f7307a95dacb14563124643e4988587cdb4783dbf1559b7452"

# 設定 Header (這就是瀏覽器缺少的通行證)
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_list_models():
    """ 測試 1: 查詢伺服器有哪些模型可以用 """
    print("正在查詢可用模型...")
    try:
        # Ollama 的標準路徑是 /api/tags
        response = requests.get(f"{BASE_URL}/api/tags", headers=headers)
        
        if response.status_code == 200:
            models = response.json().get('models', [])
            print("✅ 成功連線！伺服器上有這些模型：")
            for m in models:
                print(f" - {m['name']}")
            return models[0]['name'] if models else None
        else:
            print(f"❌ 查詢失敗: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ 連線錯誤: {e}")
        return None

def test_chat(model_name):
    """ 測試 2: 傳送簡單對話 """
    print(f"\n正在測試對話 (使用模型: {model_name})...")
    
    # Ollama 的標準對話路徑是 /api/chat
    url = f"{BASE_URL}/api/chat"
    
    # 這是我們要傳給 AI 的資料
    payload = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": "Hello! Please introduce yourself in one sentence."}
        ],
        "stream": False # 關閉串流模式，讓它一次回傳比較好讀
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            ai_reply = result['message']['content']
            print("✅ AI 回覆成功：")
            print("-" * 20)
            print(ai_reply)
            print("-" * 20)
        else:
            print(f"❌ 對話失敗: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ 錯誤: {e}")

if __name__ == "__main__":
    # 1. 先查模型
    first_model = test_list_models()
    
    # 2. 如果有查到模型，就拿第一個來測試對話
    if first_model:
        test_chat(first_model)
    else:
        # 如果查不到，通常預設可能是 'llama3' 或 'llama2'，你可以手動改成 'llama3' 試試看
        print("\n無法自動取得模型列表，嘗試盲測 'llama3'...")
        test_chat("llama3")