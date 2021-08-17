import pytest
from starlette.testclient import TestClient

from home_warehouse_api.main import app


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


def test_ping(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}
