from pathlib import Path
import pytest
from app import create_app

@pytest.fixture()
def app():
    """initialize flask app for testing"""
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app

@pytest.fixture()
def client(app):
    """returns test_client for testing"""
    return app.test_client()

resources = Path(__file__).parent / "resources"

def test_hello(client):
    response = client.get("/hello")
    assert response.status_code == 200

def test_register(client):
    response = client.post("/auth/register")
    assert response.status_code == 400

def test_login(client):
    response = client.post("/auth/login")
    assert response.status_code == 400

def test_Upload(client):
    response = client.post("/Maschine/Upload")
    assert response.status_code == 415

def test_Upload(client):
    response = client.post("/Maschine/ConnectMaschine")
    assert response.status_code == 415

def test_Upload(client):
    response = client.post("/Maschine/New")
    assert response.status_code == 415

def test_test(client):
    response = client.post("/profile/test")
    assert response.status_code == 401

def test_test(client):
    response = client.post("/profile/getMaschines")
    assert response.status_code == 401

def test_test(client):
    response = client.post("/profile/getMaschineData")
    assert response.status_code == 401