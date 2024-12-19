from typing import List, Optional
from pydantic import BaseModel

class NotificationBase(BaseModel):
    content: str

class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    id: int
    user_id: int
    timestamp: Optional[str]

    class Config:
        orm_mode = True
