import ldap3
from flask import current_app
from app.models import User
from app import db

def ldap_authenticate(username, password):
    """
    Аутентификация пользователя через Active Directory
    """
    server = ldap3.Server(current_app.config['LDAP_SERVER'])
    conn = ldap3.Connection(
        server,
        user=f"{current_app.config['LDAP_DOMAIN']}\\{username}",
        password=password,
        auto_bind=False
    )

    try:
        conn.bind()
        return True
    except ldap3.core.exceptions.LDAPBindError:
        return False
    finally:
        conn.unbind()

def sync_user_from_ldap(username):
    """
    Синхронизация пользователя из AD в локальную базу (без пароля)
    """
    if not User.query.filter_by(username=username).first():
        user = User(username=username, role="user", access_level=1)
        db.session.add(user)
        db.session.commit()
    return User.query.filter_by(username=username).first()