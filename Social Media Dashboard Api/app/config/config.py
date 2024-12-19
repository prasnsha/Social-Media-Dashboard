import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME : str = "Social Media Dashboard Api"
    DATABASE_URL : str = os.getenv("DATABASE_URL")
    JWT_SECRET : str = os.getenv("JWT_SECRET")
    JWT_ALGORITHM : str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES : int = 15

    class Config:
        env_file = ".env"

settings = Settings()

print(f"Loaded JWT_SECRET: {settings.JWT_SECRET}")
print(f"Loaded JWT_ALGORITHM: {settings.JWT_ALGORITHM}")