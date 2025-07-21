from fastapi import APIRouter, Depends
from models.user import User
from security import get_current_user

router = APIRouter()



@router.get("/profile")
def read_profile(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username, "email": current_user.email}


# 前端帶著這個 token 呼叫 /profile 範例：

# GET /profile
# Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9....