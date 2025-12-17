#from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import app
from core.auth import get_current_user

#app = FastAPI()
client = TestClient(app)

class FakeUser:
    uuid = "123e4567-e89b-12d3-a456-426614174000"
    email = "test@example.com"
    first_name = "Jean"
    last_name = "Test"

def override_get_current_user():
    return FakeUser()

def test_me_authenticated():
    app.dependency_overrides[get_current_user] = override_get_current_user

    response = client.get("/users/me")

    assert response.status_code == 200
    assert response.json() == {
        "uuid": FakeUser.uuid,
        "email": FakeUser.email,
        "first_name": FakeUser.first_name,
        "last_name": FakeUser.last_name,
    }

    app.dependency_overrides.clear()
