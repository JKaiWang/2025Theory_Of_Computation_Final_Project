# src/config.py

# 你的 API 金鑰
API_KEY = "83a2443ff6bc54f7307a95dacb14563124643e4988587cdb4783dbf1559b7452"

# 助教的伺服器網址
BASE_URL = "https://api-gateway.netdb.csie.ncku.edu.tw"

# 我們剛剛測試成功的模型名稱
MODEL_NAME = "gpt-oss:120b"

# API Header 設定
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}