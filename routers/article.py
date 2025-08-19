from fastapi import FastAPI, Header, HTTPException, APIRouter, Depends
from typing import List, Optional
import jwt  # pip install pyjwt


from schemas.schema import AddArticleRequest

from security import get_current_user
from database import get_db
from models.models import Word, User

# 匯入 SQLAlchemy 的 Session 類型，用於與資料庫互動
from sqlalchemy.orm import Session

# 建立一個 APIRouter 實例，讓這個檔案可以獨立作為路由模組
router = APIRouter()


@router.get('/articles')
def get_articles(current_user:User = Depends(get_current_user), db: Session = Depends(get_db)):
    aricles = db.query(Article).filter(Article.user_id == current_user.id).all()

    return {'message': '文章查詢成功', 'account': current_user.username, 'articles': articles}


@router.post('/article')
def add_article(current_user:User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user:
        return {"message": "請先登入"}

    new_article = Article(user_id = current_user.id, content = req.content, tags_css = req.tags_css)
    db.add(new_article)
    db.commit()
    db.refresh(new_article) ## 沒有要回傳值，其實可以不用refresh

    return {'message': '文章新增成功!', 'account': current_user.username, 'article':{'title': req.title, 'content': req.content}}

