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

# 匯入密碼雜湊function
from security import hash_password



hashed_pw = hash_password(req.password)
# 註冊feature包含：
# 宣告路由字串
# 定義資料驗證schema
# 定義連接資料庫
# 確認使用者是否存在，存在的話raise HTTPException拋出錯誤碼和錯誤訊息告知使用者已存在
# 定義加密物件 (不用放在路由function裡，可放在外層避免重複呼叫)
# 取得加密過後的密碼
# 建立一個使用者資料物件 (model裡面的物件)，傳入使用者帳號與密碼 (其他的可自行添加)
# 將new_user物件加入資料庫session
# db.commit將資料庫session的變更提交至資料庫
# refresh資料庫session，讓資料為最新狀態 (包含DB自動生成的欄位，例如id)


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
    hashed_pw = hash_password(req.password)

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