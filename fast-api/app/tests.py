from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_similarity_unicorn_error():
    response = client.post("/skills/similarity", json={"name": "unicorn"})
    assert response.status_code == 418
    assert response.json() == {"message": "Oops! unicorn did something. There goes a rainbow..."}
