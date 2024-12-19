from sqlalchemy.orm import Session
from models import models

class PostRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_post(self, post: models.Post):
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def get_posts(self, skip: int = 0, limit: int = 10):
        return self.db.query(models.Post).offset(skip).limit(limit).all()

    def get_post(self, post_id: int):
        return self.db.query(models.Post).filter(models.Post.id == post_id).first()

    def update_post(self, post: models.Post):
        self.db.commit()
        self.db.refresh(post)
        return post

    def delete_post(self, post: models.Post):
        self.db.delete(post)
        self.db.commit()
        return post
