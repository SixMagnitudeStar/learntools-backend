from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db

# from database import get_db

from datetime import datetime, timedelta
import jwt
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

from passlib.context import CryptContext

from fastapi.security import OAuth2PasswordBearer
# oauth2_scheme 是一個 FastAPI 的「依賴元件」，它的作用是：
# 從請求中「自動提取」HTTP Header 中的 Bearer Token。

## 產生token
# jwt token組成包含：1. 使用者名稱與到期資訊的資料  2. 密鑰 3. 演算法

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)




# 設定加密上下文，這裡指定使用 bcrypt 演算法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



##

#  # ✅ 建立 OAuth2PasswordBearer 實例（這一行是關鍵）
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login",
    auto_error=False  # 這會讓它在沒有 token 時返回 None 而不是拋出異常
)

# oauth2_scheme 主要有兩個核心功能：

# 實際的請求驗證功能

# 自動生成 API 文檔（Swagger UI）


## token驗證       ## Depends是依賴，他會自動呼叫那些functino並回傳值給定義好的參數
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user