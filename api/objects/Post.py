from sqlalchemy import Table, Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Post(Base):
    __tablename__ = "posts"
    id = Column('id', Integer, primary_key = True)
    title =Column('title', String)
    link = Column('link', String)
    posted =  Column('posted', Integer)
    subreddits =  Column('subreddits', String)
    scheduled =  Column('scheduled', DateTime)