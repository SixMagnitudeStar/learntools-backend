from pydantic import BaseModel
from typing import List, Dict, Optional


class RegisterRequest(BaseModel):
    username: str
    password: str
    nickname: str


class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AddWordRequest(BaseModel):
    word: str


class AddArticleRequest(BaseModel):
    title: str
    content: str
    note: str



class AddArticleBlockRequest(BaseModel):
    index: int
    text: str
    text_type: str
    previous_index: Optional[int] = None
    next_index: Optional[int] = None
    # previous_index: int
    # next_index: int

class AddArticleBlocksRequest(BaseModel):
    blocks: List[AddArticleBlockRequest]

class AddMarkedWordRequest(BaseModel):
    article_id: int
    word: str



class ArticleBlockRes(BaseModel):
    id: int
    text: str
    text_type: str

    previous_index: Optional[int] = None
    next_index: Optional[int] = None

    class Config:
        orm_mode = True

class ArticleRes(BaseModel):
    id: int
    title: str
    content: str
    note: Optional[str] = ''
    blocks: List[ArticleBlockRes] = []

    class Config:
        orm_mode = True


class AddArticleWithBlocksRequest(BaseModel):
    title: str
    content: str
    note: str
    blocks: List[AddArticleBlockRequest] = []   # 預設空陣列