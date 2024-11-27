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

def test_ops_upload(client):
    user = User(email="ops@example.com", password="hashed", role="ops")
    db.session.add(user)
    db.session.commit()