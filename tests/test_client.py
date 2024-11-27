import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
    yield app
    db.session.remove()

@pytest.fixture
def client(app):
    return app.test_client()

def test_client_signup(client):
    data = {"email": "testclient@example.com", "password": "securepassword"}
    response = client.post('/api/auth/signup', json=data)
    assert response.status_code == 201
    assert "verification_link" in response.json

def test_client_file_list(client):
    response = client.get('/api/client/files')
    assert response.status_code == 401  # No token provided

def test_client_download(client):
    response = client.get('/api/client/download/1')
    assert response.status_code == 401  # Unauthorized for unauthenticated users
