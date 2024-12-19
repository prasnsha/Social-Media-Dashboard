from fastapi import FastAPI
from core.database import engine, Base
from api import user, post, follow, notification, auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, tags=['auth'])
app.include_router(user.router, prefix="/api/v1", tags=["users"])
app.include_router(post.router, prefix="/api/v1", tags=["posts"])
app.include_router(follow.router, prefix="/api/v1", tags=["follows"])
app.include_router(notification.router, prefix="/api/v1", tags=["notifications"])

from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)