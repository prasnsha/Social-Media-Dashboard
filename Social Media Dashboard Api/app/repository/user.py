from sqlalchemy.orm import Session
from datetime import timedelta
from models import models
from schemas import auth
from core.security import get_password_hash, verify_password, create_access_token
from config.config import settings

class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str):
        return self.db.query(models.User).filter(models.User.username == username).first()

    def create_user(self, user: auth.UserCreate):
        hashed_password = get_password_hash(user.password)
        db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def authenticate_user(self, username: str, password: str):
        user = self.get_user_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def create_access_token(self, user: models.User):
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )