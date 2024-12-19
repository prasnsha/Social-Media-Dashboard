from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import HTTPException, Depends, Request
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from core.database import get_db
from config.config import settings
from models import models
from schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_ALGORITHM = "HS256"

class JWTBearer:
    def __init__(self, auto_error: bool = True):
        self.auto_error = auto_error

    async def __call__(self, request: Request):
        token = request.headers.get("Authorization")
        if token is None or not token.startswith("Bearer "):
            if self.auto_error:
                raise HTTPException(status_code=403, detail="Invalid authorization header")
            return None
        token = token.split(" ")[1]
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[JWT_ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=403, detail="Invalid token")
            return username
        except (JWTError, ValidationError):
            if self.auto_error:
                raise HTTPException(status_code=403, detail="Invalid token")
            return None

jwt_bearer = JWTBearer()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_current_user(db: Session = Depends(get_db), username: str = Depends(jwt_bearer)):
    user = get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=401, detail="Inactive user")
    return current_user

def get_current_superuser(current_user: models.User = Depends(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return current_user
