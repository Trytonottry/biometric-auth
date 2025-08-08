from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(50), default="user")  # user, admin, guest
    access_level = db.Column(db.Integer, default=1)  # 1-5
    face_template = db.Column(db.String(255))  # путь к зашифрованному файлу
    fingerprint_hash = db.Column(db.String(255))  # хэш отпечатка
    iris_template = db.Column(db.String(255))     # путь к шаблону радужки
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

class AuthLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    method = db.Column(db.String(50))  # face, fingerprint, iris
    success = db.Column(db.Boolean)
    ip_address = db.Column(db.String(45))
    anomaly_flag = db.Column(db.Boolean, default=False)

class UserInteractionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event = db.Column(db.String(50))  # keypress, mousemove, click
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    duration = db.Column(db.Float)   # ms
    speed = db.Column(db.Float)      # px/sec