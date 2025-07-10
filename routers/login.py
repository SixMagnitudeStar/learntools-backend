from dotenv import load_dotenv
from pathlib import Path
import os



# 找到專案根目錄的 .env 路徑
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
# load_dotenv()

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import jwt
from datetime import datetime, timedelta

from database import SessionLocal
from models.user import User
from schemas.user import LoginRequest, TokenResponse



from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

from database import get_db

# SECRET_KEY = os.getenv("SECRET_KEY")


## 抓環境變數，沒有值就給第二個參數的預設值
# ALGORITHM = os.getenv("ALGORITHM", "HS256")
# ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# SECRET_KEY = "your_secret_key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

# Dependency：取得資料庫 session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

@router.post("/login", response_model=TokenResponse)
def login(login_req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == login_req.username).first()
    print(f"SECRET_KEY: {SECRET_KEY} (type: {type(SECRET_KEY)})")
    print(f"user: {user}")
    if user:
        print(f"user.username: {user.username} (type: {type(user.username)})")
    else:
        print("user is None")
    if not user or user.password != login_req.password:
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode({"sub": user.username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}