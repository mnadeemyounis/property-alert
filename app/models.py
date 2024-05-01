from sqlalchemy import Boolean, Column, Integer, String, DateTime

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    email_enabled = Column(Boolean, default=False)
    sms_enabled = Column(Boolean, default=False)
    created = Column(DateTime, nullable=True)
    modified = Column(DateTime, nullable=True)
