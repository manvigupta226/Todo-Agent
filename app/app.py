# app/app.py
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Optional, List
import datetime
from .db_utils import get_conn
import os

app = FastAPI(title="TODO Agent API")

class TodoIn(BaseModel):
    title: str
    description: Optional[str] = None

class TodoOut(TodoIn):
    id: int
    done: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime

# For local dev we read APP_API_KEY from env
APP_API_KEY = os.getenv("APP_API_KEY", "test_api_key")

def require_api_key(x_api_key: str = Header(...)):
    if x_api_key != APP_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/todos", response_model=TodoOut, dependencies=[Depends(require_api_key)])
def create_todo(payload: TodoIn):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "INSERT INTO todos (title, description) VALUES (%s, %s) RETURNING id, title, description, done, created_at, updated_at",
        (payload.title, payload.description),
    )
    row = cur.fetchone()
    conn.commit()
    cur.close(); conn.close()
    return row

@app.get("/todos", response_model=List[TodoOut], dependencies=[Depends(require_api_key)])
def list_todos(limit: int = 50):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, title, description, done, created_at, updated_at FROM todos ORDER BY created_at DESC LIMIT %s", (limit,))
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

@app.patch("/todos/{todo_id}", response_model=TodoOut, dependencies=[Depends(require_api_key)])
def update_todo(todo_id: int, payload: TodoIn):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        UPDATE todos SET title=%s, description=%s, updated_at=now()
        WHERE id=%s RETURNING id, title, description, done, created_at, updated_at
    """, (payload.title, payload.description, todo_id))
    row = cur.fetchone()
    if not row:
        cur.close(); conn.close()
        raise HTTPException(status_code=404, detail="Todo not found")
    conn.commit()
    cur.close(); conn.close()
    return row

@app.delete("/todos/{todo_id}", dependencies=[Depends(require_api_key)])
def delete_todo(todo_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM todos WHERE id=%s RETURNING id", (todo_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close(); conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"deleted_id": deleted[0]}
