from sqlalchemy.orm import Session
from models import models

class FollowRepository:

    def __init__(self, db: Session):
        self.db = db

    def follow_user(self, follow: models.Follow):
        self.db.add(follow)
        self.db.commit()
        self.db.refresh(follow)
        return follow

    def unfollow_user(self, follow: models.Follow):
        self.db.delete(follow)
        self.db.commit()
        return follow

    def get_followers(self, user_id: int):
        return self.db.query(models.Follow).filter_by(followed_id=user_id).all()

    def get_following(self, user_id: int):
        return self.db.query(models.Follow).filter_by(follower_id=user_id).all()
