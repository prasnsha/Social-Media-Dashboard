from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from crud import follow as crud_follow
from schemas.follow import  Follow, FollowCreate
from models import models
from core.security import get_current_user

router = APIRouter()

@router.post("/follow/", response_model=Follow)
def follow_user(follow: FollowCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    try:
        return crud_follow.follow_user(db=db, follower_id=current_user.id, followed_id=follow.followed_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/unfollow/", response_model=Follow)
def unfollow_user(follow: FollowCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    try:
        return crud_follow.unfollow_user(db=db, follower_id=current_user.id, followed_id=follow.followed_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/followers/", response_model=List[Follow])
def get_followers(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    try:
        return crud_follow.get_followers(db=db, user_id=current_user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/following/", response_model=List[Follow])
def get_following(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    try:
        return crud_follow.get_following(db=db, user_id=current_user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))