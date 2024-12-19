from sqlalchemy.orm import Session
from models import models

class NotificationRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_notification(self, notification: models.Notification):
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def get_notifications(self, user_id: int):
        return self.db.query(models.Notification).filter_by(user_id=user_id).all()
