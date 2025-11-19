import os, requests

APP_BASE = os.getenv("APP_BASE_URL", "http://localhost:8000")
APP_API_KEY = os.getenv("APP_API_KEY", "test_api_key")

def list_todos(limit: int = 50):
    url = APP_BASE.rstrip("/") + f"/todos?limit={int(limit)}"
    headers = {"x-api-key": APP_API_KEY}
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    return r.json()
