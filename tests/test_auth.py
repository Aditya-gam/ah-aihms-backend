import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    return app.test_client()


def test_status_endpoint(client):
    response = client.get('/api/auth/status')
    assert response.status_code == 200
    assert response.json['status'] == 'auth route working'
