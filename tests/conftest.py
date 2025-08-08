import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        db.create_all()

        # Тестовый пользователь
        user = User(username="testuser", role="user", access_level=1)
        db.session.add(user)
        db.session.commit()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.drop_all()