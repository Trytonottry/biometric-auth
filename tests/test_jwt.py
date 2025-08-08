from app.api.jwt_utils import generate_jwt, verify_jwt

def test_jwt_generation_and_verification():
    user_id = 123
    token = generate_jwt(user_id)
    decoded = verify_jwt(token)
    assert decoded == user_id

def test_jwt_expired():
    from datetime import datetime, timedelta
    import jwt
    import app.config as config

    payload = {
        'user_id': 123,
        'exp': datetime.utcnow() - timedelta(hours=1),  # просрочен
        'iat': datetime.utcnow() - timedelta(hours=2)
    }
    token = jwt.encode(payload, config.Config.SECRET_KEY, algorithm='HS256')
    result = verify_jwt(token)
    assert result is None