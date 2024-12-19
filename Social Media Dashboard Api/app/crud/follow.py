from sqlalchemy.orm import Session
from models import models

def follow_user(db: Session, follower_id: int, followed_id: int):
    follow = models.Follow(follower_id=follower_id, followed_id=followed_id)
    db.add(follow)
    db.commit()
    db.refresh(follow)
    return follow

def unfollow_user(db: Session, follower_id: int, followed_id: int):
    follow = db.query(models.Follow).filter_by(follower_id=follower_id, followed_id=followed_id).first()
    if follow:
        db.delete(follow)
        db.commit()
    return follow

def get_followers(db: Session, user_id: int):
    return db.query(models.Follow).filter_by(followed_id=user_id).all()

def get_following(db: Session, user_id: int):
    return db.query(models.Follow).filter_by(follower_id=user_id).all()
