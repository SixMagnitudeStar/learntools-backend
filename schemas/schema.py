from pydantic import BaseModel
from typing import List, Dict


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
 ##   tags_css: List[Dict[str, str]]  = []  # 預設空列表


class AddArticleBlockRequest(Base):
    article_id: int
    index: int
    text: str
    text_type: str
    previous_id: int
    next_id: int

class AddArticleBlocksRequest(Base):
    blocks: List[AddArticleBlockRequest]

class AddMarkedWordRequest(BaseModel):
    article_id: int
    word: str