from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger

db = SQLAlchemy()
migrate = Migrate()
swagger = Swagger()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../instance/config.py')

    db.init_app(app)
    migrate.init_app(app, db)
    swagger.init_app(app)

    # Подключаем API и Blueprint
    from app.api import api, add_resources
    api.init_app(app)
    add_resources(api)

    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    # Настройка Swagger
    app.config['SWAGGER'] = {
        'title': 'Biometric Auth API',
        'uiversion': 3,
        'description': 'API для биометрической аутентификации с JWT, liveness и плагинами'
    }

    return app