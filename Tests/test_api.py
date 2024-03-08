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
    """this procedure tests the Test-API /hello"""
    response = client.get("/hello")
    assert response.status_code == 200