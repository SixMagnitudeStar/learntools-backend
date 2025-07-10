from fastapi import APIRouter, Header, HTTPException
import jwt
from config import SECRET_KEY, ALGORITHM

router = APIRouter()

# 這裡用 set 模擬黑名單
blacklist = set()


    # 登出 API，使用 POST 方法，路徑為 /logout
@router.post("/logout")
async def logout(authorization: str = Header(None)):
    # 檢查是否有帶入 Authorization header，且開頭為 "Bearer "
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Authorization header missing or invalid")
    
    # 從 "Bearer <token>" 中取出 token 部分
    token = authorization.split(" ")[1]
    
    try:
        # 嘗試使用 JWT 解碼該 token，確認其有效性
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    # 若 token 已過期，回傳 401 Unauthorized
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    
    # 若 token 不合法（例如被竄改），回傳 401 Unauthorized
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # 將此合法 token 加入黑名單，表示已登出（之後驗證時會擋掉）
    blacklist.add(token)

    # 回傳成功訊息
    return {"message": "Logout successful."}