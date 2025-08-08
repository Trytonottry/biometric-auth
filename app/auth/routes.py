from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User, AuthLog
from app.auth.biometrics import authenticate_user
from app.utils.encryption import encrypt_data
from app.utils.storage import save_biometric_data
from app.auth.ldap_auth import ldap_authenticate, sync_user_from_ldap
import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if not user:
            flash("Пользователь не найден.")
            return redirect(url_for('auth.login'))

        methods = request.form.getlist('methods')
        success, logs = authenticate_user(user, methods, request.remote_addr)

        for log_data in logs:
            log = AuthLog(**log_data)
            db.session.add(log)
        db.session.commit()

        if success:
            session['user_id'] = user.id
            return redirect(url_for('auth.dashboard'))
        else:
            flash("Аутентификация не удалась.")

    return render_template('login.html')
if ldap_authenticate(username, password):
    user = sync_user_from_ldap(username)
    # продолжить биометрическую MFA

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']
        access_level = int(request.form['access_level'])

        if User.query.filter_by(username=username).first():
            flash("Пользователь уже существует.")
            return redirect(url_for('auth.register'))

        user = User(username=username, role=role, access_level=access_level)

        # Регистрация биометрии
        if 'face' in request.form:
            face_data = capture_face()
            if face:
                encrypted = encrypt_data(face_data)
                path = save_biometric_data(encrypted, username, "face.enc")
                user.face_template = path

        if 'fingerprint' in request.form:
            fp_hash = capture_fingerprint()
            user.fingerprint_hash = fp_hash

        if 'iris' in request.form:
            iris_hash = capture_iris()
            path = save_biometric_data(iris_hash.encode(), username, "iris.enc")
            user.iris_template = path

        db.session.add(user)
        db.session.commit()
        flash("Регистрация завершена!")
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))