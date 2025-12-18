from fastapi import FastAPI
from fastapi.testclient import TestClient

# Create a simple FastAPI app for testing
app = FastAPI()

# Simple endpoint for testing
@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

# Create a TestClient for the FastAPI app
client = TestClient(app)

# Test the root endpoint
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}