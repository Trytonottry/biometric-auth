from flask_restful import Resource, reqparse
from flask import jsonify
from app.models import User, AuthLog
from app import db
from app.auth.biometrics import authenticate_user
from app.api.jwt_utils import generate_jwt

# Парсер для входа
login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, required=True, help="Требуется имя пользователя")
login_parser.add_argument('methods', type=str, action='append', help="Способы аутентификации")

# Парсер для регистрации
register_parser = reqparse.RequestParser()
register_parser.add_argument('username', type=str, required=True)
register_parser.add_argument('role', type=str, default='user')
register_parser.add_argument('access_level', type=int, default=1)
register_parser.add_argument('enable_face', type=bool, default=False)
register_parser.add_argument('enable_fingerprint', type=bool, default=False)
register_parser.add_argument('enable_iris', type=bool, default=False)

class LoginAPI(Resource):
    def post(self):
        args = login_parser.parse_args()
        username = args['username']
        methods = args['methods'] or []

        user = User.query.filter_by(username=username).first()
        if not user:
            return {"error": "Пользователь не найден"}, 404

        success, logs = authenticate_user(user, methods, "127.0.0.1")  # В реальности — request.remote_addr

        for log_data in logs:
            log = AuthLog(**log_data)
            db.session.add(log)
        db.session.commit()

        if success:
            token = generate_jwt(user.id)
            return {
                "success": True,
                "token": token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "role": user.role
                }
            }, 200
        else:
            return {"success": False, "message": "Ошибка аутентификации"}, 401

class RegisterAPI(Resource):
    def post(self):
        args = register_parser.parse_args()
        username = args['username']

        if User.query.filter_by(username=username).first():
            return {"error": "Имя занято"}, 400

        user = User(
            username=username,
            role=args['role'],
            access_level=args['access_level']
        )

        # Здесь можно добавить захват биометрии (в реальном времени — сложно через API)
        # Для демо — просто флаги
        db.session.add(user)
        db.session.commit()

        return {"success": True, "user_id": user.id}, 201

class UserListAPI(Resource):
    def get(self):
        users = User.query.all()
        return [{
            "id": u.id,
            "username": u.username,
            "role": u.role,
            "access_level": u.access_level,
            "has_face": bool(u.face_template),
            "has_fingerprint": bool(u.fingerprint_hash),
            "has_iris": bool(u.iris_template)
        } for u in users]

# Подключение роутов
def add_resources(api):
    api.add_resource(LoginAPI, '/api/login')
    api.add_resource(RegisterAPI, '/api/register')
    api.add_resource(UserListAPI, '/api/users')