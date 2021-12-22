"""
Post object for the declerative base
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Post(Base):
    """
    Post object for the declerative base
    Args:
        Base ([type]): the base object
    """

    __tablename__ = "posts"
    id = Column("id", Integer, primary_key=True)
    title = Column("title", String)
    link = Column("link", String)
    posted = Column("posted", Integer)
    subreddits = Column("subreddits", String)
    scheduled = Column("scheduled", DateTime)

