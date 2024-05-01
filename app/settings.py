import os

CELERY_BROKER = os.environ.get('REDIS_URL', "redis://127.0.0.1:6379/0")
CELERY_BACKEND = os.environ.get('REDIS_URL', "redis://127.0.0.1:6379/0")

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
