from fastapi import FastAPI, Header, HTTPException, APIRouter, Depends
from typing import List, Optional
import jwt  # pip install pyjwt


from schemas.schema import AddArticleRequest

from security import get_current_user
from database import get_db
from models.models import Article, User

# 匯入 SQLAlchemy 的 Session 類型，用於與資料庫互動
from sqlalchemy.orm import Session
import json

# 建立一個 APIRouter 實例，讓這個檔案可以獨立作為路由模組
router = APIRouter()


@router.get('/articles')
def get_articles(current_user:User = Depends(get_current_user), db: Session = Depends(get_db)):
    articles = db.query(Article).filter(Article.user_id == current_user.id).all()

    # 將 Article 物件 list 轉成 dict list
    articles_list = [article_to_dict(a) for a in articles]

    return {'message': '文章查詢成功', 'account': current_user.username, 'articles': articles_list}


def article_to_dict(article: Article):
    return {
        "id": article.id,
        "title": article.title,
        "content": article.content,
        # "tags_css": json.loads(article.tags_css) if article.tags_css else []
        "tags_css": article.tags_css or []
    }




@router.post('/article')
def add_article(req: AddArticleRequest,current_user:User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user:
        return {"message": "請先登入"}

    new_article = Article(user_id = current_user.id, content = req.content, tags_css = req.tags_css)
    db.add(new_article)
    db.commit()
    db.refresh(new_article) ## 沒有要回傳值，其實可以不用refresh

    return {'message': '文章新增成功!', 'account': current_user.username, 'article':{'title': req.title, 'content': req.content}}

