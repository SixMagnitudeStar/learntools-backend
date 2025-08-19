from fastapi import FastAPI, Header, HTTPException, APIRouter, Depends
from typing import List, Optional
import jwt  # pip install pyjwt


from schemas.schema import AddWordRequest

from security import get_current_user
from database import get_db
from models.models import Word, User

# 匯入 SQLAlchemy 的 Session 類型，用於與資料庫互動
from sqlalchemy.orm import Session

# 建立一個 APIRouter 實例，讓這個檔案可以獨立作為路由模組
router = APIRouter()


@router.get('/words')
def get_words(current_user:User = Depends(get_current_user), db: Session = Depends(get_db)):
    words = db.query(Word).filter(Word.account == current_user.username).all()
    word_list = [w.word for w in words]

    return {'message': '單字查詢成功!', 'account': current_user.username, 'words': word_list}


@router.post('/word')
def add_word(req: AddWordRequest, current_user: User = Depends(get_current_user), db:Session = Depends(get_db)):
    if not current_user:
        return {"message": "請先登入"}

    new_word = Word(account = current_user.username, word = req.word)
    db.add(new_word)
    db.commit()
    db.refresh(new_word)

    return {'message': '新增單字成功!', 'account': current_user.username, 'word':req.word}