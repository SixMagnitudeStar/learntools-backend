 
# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
import sqlite3

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

###############



# JWT 設定
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 請求資料模型
class LoginRequest(BaseModel):
    username: str
    password: str

# 初始化資料庫（啟動時建立資料表與預設帳號）
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    # 建立預設帳號 admin / password（如果不存在）
    cursor.execute("SELECT * FROM users WHERE username = ?", ("admin",))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "password"))
    conn.commit()
    conn.close()

# 執行資料庫初始化
init_db()

# 登入 API
@app.post("/login")
def login(login_req: LoginRequest):
    username = login_req.username
    password = login_req.password

    # 連線資料庫查詢
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row is None or row[0] != password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # 產生 JWT token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": username,
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}

