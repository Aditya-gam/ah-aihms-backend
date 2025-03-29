import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
