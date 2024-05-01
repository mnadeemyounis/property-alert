import os
from datetime import datetime
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.apis import app, get_db


if os.path.exists("./tests/sql_app.db"):
    os.remove("./tests/sql_app.db")

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
models.Base.metadata.create_all(bind=engine)


# Dependency to override get_db() in FastAPI application
@pytest.fixture(scope="module")
def override_get_db():
    def override_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_db
    yield
    app.dependency_overrides.clear()


# Create a FastAPI test client
client = TestClient(app)


# Unit tests
def test_get_all_user_preferences(override_get_db):
    response = client.get("/preferences/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user_preferences__status_404(override_get_db):
    response = client.get("/preferences/1")
    assert response.status_code == 404  # Assuming user preferences with ID 1 doesn't exist in the test database


def test_create_user_preferences(override_get_db):
    user_data = {
        "email": "test@example.com", "phone": "+921234567890", "password": "testpassword", "email_enabled": True,
        "sms_enabled": True,
    }
    response = client.post("/preferences/", json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]


def test_create_user_preferences__status_400(override_get_db):
    user_data = {
        "email": "test@example.com", "phone": "+921234567890", "password": "testpassword", "email_enabled": True,
        "sms_enabled": True,
    }
    response = client.post("/preferences/", json=user_data)
    assert response.status_code == 400  # Assuming user preferences already exists for this user


def test_get_user_preferences(override_get_db):
    response = client.get("/preferences/1")
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


def test_update_user_preferences__status_404(override_get_db):
    user_data = {
        "email": "test@example.com", "phone": "+921234567890", "password": "testpassword", "email_enabled": True,
        "sms_enabled": True,
    }
    response = client.put("/preferences/2", json=user_data)
    assert response.status_code == 404  # Assuming user preferences with ID 2 doesn't exist in the test database


def test_update_user_preferences(override_get_db):
    user_data = {
        "email": "test@example.com", "phone": "+921234567891", "password": "testpassword", "email_enabled": True,
        "sms_enabled": True,
    }
    response = client.put("/preferences/1", json=user_data)
    assert response.json()["email"] == "test@example.com"
    assert response.json()["phone"] == "+921234567891"


@patch("app.tasks.send_notification.apply_async")
def test_integration_schedule_notification(mock_apply_async):
    notification_data = {
        "user_id": 1,
        "message": "Test message",
        "notification_type": "email",
        "notification_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    }
    response = client.post("/notifications", json=notification_data)
    assert response.status_code == 200
    mock_apply_async.assert_called_once()
    assert response.json() == {"message": "Notification scheduled"}
