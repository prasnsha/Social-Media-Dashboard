from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from core.database import Base
import datetime



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    posts = relationship("Post", back_populates="owner")
    followers = relationship("Follow", back_populates="followed_user", foreign_keys='Follow.followed_id')
    following = relationship("Follow", back_populates="following_user", foreign_keys='Follow.follower_id')

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    post_type = Column(String, nullable=False)  # text, image, link
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="posts")

class Follow(Base):
    __tablename__ = 'follows'

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey('users.id'))
    followed_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    following_user = relationship("User", foreign_keys=[follower_id], back_populates="following")
    followed_user = relationship("User", foreign_keys=[followed_id], back_populates="followers")

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_read = Column(Boolean, default=False)
