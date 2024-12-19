from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from crud import notification as crud_notification
from schemas.notification import Notification, NotificationCreate
from models import models
from core.security import get_current_user


router = APIRouter()

@router.post("/notifications/", response_model=Notification)
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    try:
        return crud_notification.create_notification(db=db, user_id=current_user.id, content=notification.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/notifications/", response_model=List[Notification])
def get_notifications(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    try:
        return crud_notification.get_notifications(db=db, user_id=current_user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))