import os, requests

APP_BASE = os.getenv("APP_BASE_URL", "http://localhost:8000")
APP_API_KEY = os.getenv("APP_API_KEY", "test_api_key")

def delete_todo(id: int):
    url = APP_BASE.rstrip("/") + f"/todos/{int(id)}"
    headers = {"x-api-key": APP_API_KEY}
    r = requests.delete(url, headers=headers, timeout=10)
    r.raise_for_status()
    return r.json()
