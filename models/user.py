from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship


from models.article import Article


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    articles = relationship("Article", back_populates="user")