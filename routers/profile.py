from fastapi import APIRouter, Depends
from models.models import User
from security import get_current_user

router = APIRouter()




@router.get("/profile")  ## Depends是依賴，他會自動呼叫那些functino並回傳值給定義好的參數
# def read_profile(current_user: User = Depends(get_current_user)):
#     return {"username": current_user.username, "email": current_user.email}
def read_profile(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username, "訊息": "呼叫成功"}


# current_user後面的: User僅是型別註解


# 前端帶著這個 token 呼叫 /profile 範例：

# GET /profile
# Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9....