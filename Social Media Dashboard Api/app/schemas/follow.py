from typing import List, Optional
from pydantic import BaseModel

class FollowBase(BaseModel):
    followed_id: int

class FollowCreate(FollowBase):
    pass

class Follow(FollowBase):
    id: int
    follower_id: int
    timestamp: Optional[str]

    class Config:
        orm_mode = True