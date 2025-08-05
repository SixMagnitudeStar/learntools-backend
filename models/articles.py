
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship, declarative_base
from pydantic import BaseModel
from typing import List, Optional

from models.user.py import User 

class Article(Base):
    __tablename__ = 'articles'  # 資料庫表名

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String)

    # 假設tags_css用JSON欄位存字典
    tags_css = Column(JSON, nullable=True)

    user = relationship("User", back_populates="articles")
