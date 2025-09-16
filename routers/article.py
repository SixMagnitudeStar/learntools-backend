from fastapi import FastAPI, Header, HTTPException, APIRouter, Depends
from typing import List, Optional
import jwt  # pip install pyjwt


from schemas.schema import AddArticleRequest, AddMarkedWordRequest

from security import get_current_user
from database import get_db
from models.models import Article, User, MarkedWord

# 匯入 SQLAlchemy 的 Session 類型，用於與資料庫互動
from sqlalchemy.orm import Session
import json

# 引入排序資料desc
from sqlalchemy import desc

from fastapi import Query

# 建立一個 APIRouter 實例，讓這個檔案可以獨立作為路由模組
router = APIRouter()


## 測試用，之後要拿掉
@router.get("/testarticle")
def findarticle(db: Session = Depends(get_db)):
    articles = db.query(Article).order_by(desc(Article.id)).all()
    
    # if articles:
    #     return {'文章': articles}
    # else:
    #     return {'回答': '找不到'}
    return {'文章': articles}



@router.get('/articles')
def get_articles(current_user:User = Depends(get_current_user), db: Session = Depends(get_db)):
    articles = db.query(Article).filter(Article.user_id == current_user.id).order_by(desc(Article.id)).all()

    # 將 Article 物件 list 轉成 dict list
    articles_list = [article_to_dict(a) for a in articles]

    return {'message': '文章查詢成功', 'account': current_user.username, 'articles': articles}



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

    new_article = Article(user_id = current_user.id,title=req.title, content = req.content, tags_css = req.tags_css, note=req.note)
    db.add(new_article)
    db.commit()
    db.refresh(new_article) ## 沒有要回傳值，其實可以不用refresh

    return {'message': '文章新增成功!', 'account': current_user.username, 'article':{'title': req.title, 'content': req.content}}



@router.put('/article/{article_id}')
def update_article(
    article_id: int,
    req: AddArticleRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="請先登入")

    # 找文章
    article = db.query(Article).filter(
        Article.id == article_id,
        Article.user_id == current_user.id   # 確保只能改自己的文章
    ).first()

    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    # 更新內容
    article.title = req.title
    article.content = req.content
    article.tags_css = req.tags_css
    article.note = req.note

    db.commit()
    db.refresh(article)

    return {
        "message": "文章修改成功!",
        "article": article_to_dict(article)
    }


@router.get('/markedwords/{article_id}')
def get_markwords(
    article_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    markedwords = db.query(
        MarkedWord).filter(MarkedWord.user_id == current_user.id, 
        MarkedWord.article_id == article_id
        ).all()

    return {'message': '標記單字查詢成功!', 'words': markedwords}    


@router.post('/markedword')
def upldate_markedword(
    req: AddMarkedWordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="請先登入")
    
    new_item = MarkedWord(user_id=current_user.id, article_id=req.article_id, word=req.word)
    db.add(new_item)
    db.commit()

    return {'message':'標記單字新增成功!','account':current_user.username, 'word':req.word}




## 只刪除查詢到的第一筆
@router.delete('/markedword')
def delete_markedword(
    article_id: Optional[int] = Query(None),
    word: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="請先登入")

    if not any([article_id, word]):
        raise HTTPException(status_code=400, detail="請提供至少一個刪除條件")

    query = db.query(MarkedWord).filter(MarkedWord.user_id == current_user.id)

    if article_id is not None:
        query = query.filter(MarkedWord.article_id == article_id)
    if word is not None:
        query = query.filter(MarkedWord.word == word)

    item = query.first()  # 只取第一筆

    if not item:
        raise HTTPException(status_code=404, detail="找不到符合條件的標記單字")

    db.delete(item)
    db.commit()

    return {
        "message": "成功刪除標記單字!",
        "account": current_user.username,
        "deleted_word": item.word
    }

# @router.delete('/markedword/{id}')
# def delete_markedword(
#     id: int,
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     if not current_user:
#         raise HTTPException(status_code=401, detail="請先登入")

#     # 找出要刪除的紀錄
#     item = db.query(MarkedWord).filter_by(
#         id=id,
#         user_id=current_user.id
#     ).first()

#     if not item:
#         raise HTTPException(status_code=404, detail="找不到對應的標記單字")

#     db.delete(item)
#     db.commit()

#     return {
#         "message": "標記單字刪除成功!",
#         "account": current_user.username,
#         "word": item.word
#     }