
from fastapi import FastAPI
from database import engine, Base, SessionLocal
from models import user
from routers import login
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

###############


# 建立資料表
Base.metadata.create_all(bind=engine)

# 預設帳號 admin/password（只在啟動時建立一次）
def init_user():
    db = SessionLocal()
    if not db.query(user.User).filter_by(username="admin").first():
        db.add(user.User(username="admin", password="password"))
        db.commit()
    db.close()

init_user()

# 掛載路由
app.include_router(login.router)