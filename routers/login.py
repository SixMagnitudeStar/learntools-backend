from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from database import SessionLocal
from models.models import User
from schemas.user import LoginRequest, TokenResponse

from database import get_db
from security import verify_password, create_access_token

router = APIRouter()



# @router.post("/login", response_model=TokenResponse)
# def login(login_req: LoginRequest, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == login_req.username).first()
#     print(f"SECRET_KEY: {SECRET_KEY} (type: {type(SECRET_KEY)})")
#     print(f"user: {user}")
#     if user:
#         print(f"user.username: {user.username} (type: {type(user.username)})")
#     else:
#         print("user is None")
#     if not user or user.password != login_req.password:
#         raise HTTPException(status_code=401, detail="Invalid username or password.")

#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     token = jwt.encode({"sub": user.username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
#     return {"access_token": token, "token_type": "bearer"}



@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    """
    使用者登入：產生 JWT Token
    """
    user = db.query(User).filter(User.username == req.username).first()
    if not user or not verify_password(req.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password.")

    # 產生 JWT token
    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}


# from fastapi.security import OAuth2PasswordRequestForm

# @router.post("/login")
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == form_data.username).first()
#     if not user or not verify_password(form_data.password, user.password):
#         raise HTTPException(status_code=400, detail="Invalid username or password.")

#     access_token = create_access_token(data={"sub": user.username})
#     return {"access_token": access_token, "token_type": "bearer"}


