from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship, declarative_base
from pydantic import BaseModel
from typing import List, Optional

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    nickname = Column(String)

    articles = relationship("Article", back_populates="user")


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    note = Column(String)

    content = Column(String)
    tags_css = Column(JSON, nullable=True)

    user = relationship("User", back_populates="articles")
    marked_words = relationship("MarkedWord")

class MarkedWord(Base):
    __tablename__ = 'marked_words'
    id = Column(Integer, primary_key=True)   # 流水號
  
    user_id = Column(Integer, ForeignKey('users.id'))

    # 這個 mark的單字屬於哪篇文章
    article_id = Column(Integer, ForeignKey('articles.id')) 
    word = Column(String)                    # mark 的單字


class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    word = Column(String)


class testmodel(Base):
    __tablename__ = 'testmodel'

    id = Column(Integer, primary_key=True, index=True)

    m = Column(String)
    a = Column(String)
    c = Column(String)

# class Note(Base):
#     __tablename__ = 'notes'

#     id = Column(Integer, primary_key = True, index=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     article_id = Column(Integer, ForeignKey('articles.id'))

#     text = Column(String)