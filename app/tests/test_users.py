from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import get_current_user

# Create a TestClient for the FastAPI app
client = TestClient(app)

# Test the /users/me endpoint with a mocked authenticated user
class FakeUser:
    uuid = "123e4567-e89b-12d3-a456-426614174000"
    email = "test@example.com"
    first_name = "Jean"
    last_name = "Test"

# Override the get_current_user dependency to return a fake user
def override_get_current_user():
    return FakeUser()

# Test the /users/me endpoint
def test_me_authenticated():

    # Override the dependency
    app.dependency_overrides[get_current_user] = override_get_current_user

    # Make a request to the /users/me endpoint
    response = client.get("/users/me")

    # Assert the response
    assert response.status_code == 200
    assert response.json() == {
        "uuid": FakeUser.uuid,
        "email": FakeUser.email,
        "first_name": FakeUser.first_name,
        "last_name": FakeUser.last_name,
    }

    # Clear the dependency overrides after the test
    app.dependency_overrides.clear()