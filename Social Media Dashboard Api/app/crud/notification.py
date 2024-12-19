from sqlalchemy.orm import Session
from models import models

def create_notification(db: Session, user_id: int, content: str):
    notification = models.Notification(user_id=user_id, content=content)
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

def get_notifications(db: Session, user_id: int):
    return db.query(models.Notification).filter_by(user_id=user_id).all()
