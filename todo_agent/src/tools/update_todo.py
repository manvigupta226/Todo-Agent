import os, requests

APP_BASE = os.getenv("APP_BASE_URL", "http://localhost:8000")
APP_API_KEY = os.getenv("APP_API_KEY", "test_api_key")

def update_todo(id: int, title: str = None, description: str = None):
    url = APP_BASE.rstrip("/") + f"/todos/{int(id)}"
    headers = {"x-api-key": APP_API_KEY}
    body = {}
    if title is not None:
        body["title"] = title
    if description is not None:
        body["description"] = description
    r = requests.patch(url, json=body, headers=headers, timeout=10)
    r.raise_for_status()
    return r.json()
