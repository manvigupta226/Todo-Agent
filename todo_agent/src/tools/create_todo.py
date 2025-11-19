import os, requests

APP_BASE = os.getenv("APP_BASE_URL", "http://localhost:8000")
APP_API_KEY = os.getenv("APP_API_KEY", "test_api_key")

def create_todo(title: str, description: str = None):
    url = APP_BASE.rstrip("/") + "/todos"
    headers = {"x-api-key": APP_API_KEY}
    payload = {"title": title, "description": description}
    r = requests.post(url, json=payload, headers=headers, timeout=10)
    r.raise_for_status()
    return r.json()
