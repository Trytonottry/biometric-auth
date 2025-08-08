from app.models import User, AuthLog
from app.modules.face_recognition import verify_face, capture_face
from app.modules.fingerprint import verify_fingerprint, capture_fingerprint
from app.modules.iris import verify_iris, capture_iris
from app.modules.anomaly_detection import detect_anomaly
from app.modules.plugins import load_plugins
from app.utils.alerts import alert_admin
from app import db
from datetime import datetime

# Загружаем плагины (voice, gait и др.)
PLUGINS = load_plugins()

def authenticate_user(user: User, methods: list, ip: str = "127.0.0.1", liveness_verified: bool = False):
    """
    Основная функция биометрической аутентификации.

    :param user: объект User
    :param methods: список методов ['face', 'fingerprint', 'iris', 'voice']
    :param ip: IP-адрес клиента
    :param liveness_verified: прошёл ли пользователь liveness detection
    :return: (успех: bool, логи: list, токен: str или None)
    """
    if not methods:
        return False, [], None

    passed = []
    log_entries = []
    token = None

    # Проверяем каждый метод
    for method in methods:
        success = False

        try:
            if method == "face":
                if not liveness_verified:
                    # Без проверки "живости" лицо не принимается
                    success = False
                else:
                    face_data = capture_face()
                    if face_data and verify_face(user, face_data):
                        success = True

            elif method == "fingerprint":
                fp_hash = capture_fingerprint()
                if verify_fingerprint(user, fp_hash):
                    success = True

            elif method == "iris":
                iris_hash = capture_iris()
                if verify_iris(user, iris_hash):
                    success = True

            elif method in PLUGINS:
                # Плагины: voice, gait и др.
                success = PLUGINS[method](user, None)  # можно передать данные

            else:
                success = False

        except Exception as e:
            print(f"Ошибка при аутентификации методом {method}: {e}")
            success = False

        # Проверка аномалии (если вход успешен)
        anomaly = False
        if success:
            anomaly = detect_anomaly(user.id, method, ip)
            if anomaly:
                alert_admin(f"Подозрительный вход: {user.username} через {method} с IP {ip}")

        # Логируем попытку
        log_entry = AuthLog(
            user_id=user.id,
            method=method,
            success=success,
            ip_address=ip,
            anomaly_flag=anomaly
        )
        log_entries.append(log_entry)
        db.session.add(log_entry)

        if success:
            passed.append(method)

    # Сохраняем логи
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Ошибка при сохранении логов: {e}")

    # Успех, если хотя бы один метод прошёл
    overall_success = len(passed) > 0

    # Генерируем JWT только при успехе
    if overall_success:
        from app.api.jwt_utils import generate_jwt
        token = generate_jwt(user.id)
        user.last_login = datetime.utcnow()
        db.session.commit()

    return overall_success, log_entries, token