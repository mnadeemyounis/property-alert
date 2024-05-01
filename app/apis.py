from datetime import datetime
from typing import List
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import SessionLocal, engine
from app.tasks import send_notification

models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Property Alert Application")


# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Example user preferences storage (can be replaced with a database)
DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"


class Notification(BaseModel):
    user_id: int
    message: str
    notification_type: str
    notification_time: Optional[datetime] = None


@app.post("/notifications")
async def schedule_notification(notification: Notification, db: Session = Depends(get_db)):
    """
    Endpoint to schedule notifications.
    """
    db_user_preferences = jsonable_encoder(crud.get_user(db, user_id=notification.user_id))

    # Push notification task to Celery queue
    task = send_notification.apply_async(args=(
        notification.user_id, notification.message, notification.notification_type,
        notification.notification_time.strftime(DATE_TIME_FORMAT)
    ), kwargs=dict(
        user_preferences=db_user_preferences
    ))
    print(task.state, task.result)
    return {"message": "Notification scheduled"}


@app.get("/preferences/", response_model=List[schemas.User])
def get_all_user_preferences(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/preferences/{user_id}", response_model=schemas.User)
def get_user_preferences(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User preferences not found")
    return db_user


@app.post("/preferences/", response_model=schemas.User)
def create_user_preferences(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User preferences already exists for this user")
    return crud.create_user(db=db, user=user)


@app.put("/preferences/{user_id}", response_model=schemas.User)
def update_user_preferences(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User preferences not found")
    return crud.update_user(db=db, user_id=user_id, user=user)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
