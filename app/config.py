from pydantic_settings import BaseSettings
import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
ENV_FILE = os.path.join(BASE_DIR, ".env")

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str
    SECRET_KEY: str
    ALGORITHM: str
    PROJECT_NAME: str = "Online Course Enrollment System"
    class Config:
        env_file = ENV_FILE
        ENV_FILE_ENCODING = "utf-8"

settings = Settings()
