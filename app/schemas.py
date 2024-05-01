from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    phone: str
    email_enabled: bool
    sms_enabled: bool


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
