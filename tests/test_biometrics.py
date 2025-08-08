import pytest
from app.auth.biometrics import authenticate_user
from app.models import User

def test_face_auth_success(client):
    user = User.query.filter_by(username="testuser").first()
    success, logs, token = authenticate_user(
        user=user,
        methods=["face"],
        ip="192.168.1.1",
        liveness_verified=True
    )
    assert success  # Имитация успешного распознавания
    assert len(logs) == 1
    assert logs[0].success is True
    assert token is not None

def test_face_auth_without_liveness(client):
    user = User.query.filter_by(username="testuser").first()
    success, logs, token = authenticate_user(
        user=user,
        methods=["face"],
        ip="192.168.1.1",
        liveness_verified=False
    )
    assert not success
    assert logs[0].success is False