from datetime import date
from pathlib import Path
import sqlite3
from urllib.parse import quote
import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("STUDYDECK_DB_PATH", BASE_DIR.parent / "studydeck.db"))
app = FastAPI(title="Study Deck")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as conn:
        conn.executescript("""CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY, nickname TEXT NOT NULL, title TEXT NOT NULL, completed INTEGER NOT NULL DEFAULT 0); CREATE TABLE IF NOT EXISTS attendance (id INTEGER PRIMARY KEY, nickname TEXT NOT NULL, attended_on TEXT NOT NULL, UNIQUE(nickname, attended_on));""")

init_db()

def layout(content):
    return HTMLResponse(f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Study Deck</title><link rel="stylesheet" href="/static/style.css"></head><body><main><h1>Study Deck</h1>{content}</main></body></html>''')

def dashboard(nickname):
    with db() as conn:
        todos = conn.execute("SELECT * FROM todos WHERE nickname = ? ORDER BY id DESC", (nickname,)).fetchall()
        attendance = conn.execute("SELECT attended_on FROM attendance WHERE nickname = ? ORDER BY attended_on DESC", (nickname,)).fetchall()
    todo_html = "".join(f'<li class="{"done" if t["completed"] else ""}">{t["title"]} <form method="post" action="/todos/{t["id"]}/toggle"><input type="hidden" name="nickname" value="{nickname}"><button>완료</button></form> <form method="post" action="/todos/{t["id"]}/delete"><input type="hidden" name="nickname" value="{nickname}"><button>삭제</button></form></li>' for t in todos)
    attendance_html = "".join(f'<li>{a["attended_on"]}</li>' for a in attendance)
    return f'''<p>안녕하세요, {nickname}님!</p><section><h2>할 일</h2><form method="post" action="/todos"><input type="hidden" name="nickname" value="{nickname}"><input name="title" required placeholder="할 일 입력"><button>추가</button></form><ul>{todo_html or "<li>할 일이 없습니다.</li>"}</ul></section><section><h2>출석</h2><form method="post" action="/attendance"><input type="hidden" name="nickname" value="{nickname}"><button>오늘 출석 체크</button></form><ul>{attendance_html or "<li>출석 기록이 없습니다.</li>"}</ul></section>'''

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    nickname = request.query_params.get("nickname", "").strip()
    if nickname:
        return layout(dashboard(nickname))
    return layout('<section><h2>별명 입력</h2><form id="nickname-form"><input id="nickname" required maxlength="40" placeholder="별명"><button>시작</button></form><script src="/static/app.js"></script></section>')

def redirect_home(nickname):
    return RedirectResponse(f"/?nickname={quote(nickname)}", 303)

@app.post("/todos")
def add_todo(nickname: str = Form(...), title: str = Form(...)):
    with db() as conn: conn.execute("INSERT INTO todos(nickname,title) VALUES (?,?)", (nickname.strip(), title.strip()))
    return redirect_home(nickname)

@app.post("/todos/{todo_id}/toggle")
def toggle_todo(todo_id: int, nickname: str = Form(...)):
    with db() as conn: conn.execute("UPDATE todos SET completed = 1 - completed WHERE id = ? AND nickname = ?", (todo_id, nickname))
    return redirect_home(nickname)

@app.post("/todos/{todo_id}/delete")
def delete_todo(todo_id: int, nickname: str = Form(...)):
    with db() as conn: conn.execute("DELETE FROM todos WHERE id = ? AND nickname = ?", (todo_id, nickname))
    return redirect_home(nickname)

@app.post("/attendance")
def check_attendance(nickname: str = Form(...)):
    with db() as conn: conn.execute("INSERT OR IGNORE INTO attendance(nickname, attended_on) VALUES (?,?)", (nickname, date.today().isoformat()))
    return redirect_home(nickname)
