from fastapi import APIRouter, Depends
from models import models
from core.security import get_current_active_user


router = APIRouter()


@router.get("/me/")
async def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user
