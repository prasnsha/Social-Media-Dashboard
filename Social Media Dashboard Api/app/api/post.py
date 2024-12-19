from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from crud import post as crud_post
from schemas.post import PostCreate, Post
from models import models
from core.security import get_current_user

router = APIRouter()

@router.post("/posts/", response_model=Post)
def create_post(post:PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    try:
        return crud_post.create_post(db=db, post=post, user_id=current_user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/posts/", response_model=List[Post])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        posts = crud_post.get_posts(db, skip=skip, limit=limit)
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/posts/{post_id}", response_model=Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    try:
        db_post = crud_post.get_post(db, post_id=post_id)
        if db_post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        return db_post
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/posts/{post_id}", response_model=Post)
def update_post(post_id: int, post:PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    try:
        db_post = crud_post.get_post(db, post_id=post_id)
        if db_post is None or db_post.owner_id != current_user.id:
            raise HTTPException(status_code=404, detail="Post not found or not authorized")
        return crud_post.update_post(db=db, post_id=post_id, post=post)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/posts/{post_id}", response_model=Post)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    try:
        db_post = crud_post.get_post(db, post_id=post_id)
        if db_post is None or db_post.owner_id != current_user.id:
            raise HTTPException(status_code=404, detail="Post not found or not authorized")
        return crud_post.delete_post(db=db, post_id=post_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))