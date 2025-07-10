# 匯入 FastAPI 所需模組
from fastapi import APIRouter, Depends, HTTPException

# 匯入 SQLAlchemy 的 Session 類型，用於與資料庫互動
from sqlalchemy.orm import Session

# 匯入密碼加密工具，這裡使用 passlib 提供的 bcrypt 封裝
from passlib.context import CryptContext

# 匯入資料庫 session dependency
from database import get_db

# 匯入使用者資料表模型
from models import User

# 匯入註冊請求的資料格式定義
from schemas import RegisterRequest

# 建立一個 APIRouter 實例，讓這個檔案可以獨立作為路由模組
router = APIRouter()

# 設定加密上下文，這裡指定使用 bcrypt 演算法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 定義一個 POST 請求的 API 路由 /register
@router.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    """
    註冊新使用者：
    - 檢查帳號是否已存在
    - 雜湊密碼後儲存到資料庫
    """

    # 查詢資料庫，看該使用者名稱是否已存在
    if db.query(User).filter(User.username == req.username).first():
        # 如果存在，丟出 400 錯誤（Bad Request）
        raise HTTPException(status_code=400, detail="Username already exists.")

    # 使用 bcrypt 雜湊密碼
    hashed_pw = pwd_context.hash(req.password)

    # 建立一個新的使用者資料物件
    new_user = User(username=req.username, password=hashed_pw)

    # 將使用者加入資料庫 session 中
    db.add(new_user)
    # 提交變更（實際寫入資料庫）
    db.commit()
    # 更新 new_user 為最新狀態（包含 DB 自動生成的欄位，例如 id）
    db.refresh(new_user)

    # 回傳成功訊息
    return {"message": "User registered successfully."}