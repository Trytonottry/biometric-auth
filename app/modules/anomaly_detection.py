from sklearn.ensemble import IsolationForest
import numpy as np
from app.models import AuthLog
from datetime import datetime, timedelta

def detect_anomaly(user_id, method, ip):
    # Анализ: сколько попыток за последние 5 минут?
    five_min_ago = datetime.utcnow() - timedelta(minutes=5)
    recent = AuthLog.query.filter(
        AuthLog.user_id == user_id,
        AuthLog.timestamp > five_min_ago
    ).count()

    # Признаки: частота, метод, IP
    features = np.array([[recent, hash(method) % 100, hash(ip) % 100]])

    iso_forest = IsolationForest(contamination=0.1)
    # В реальности обучать на исторических данных
    prediction = iso_forest.fit_predict(features)

    return prediction[0] == -1  # -1 = аномалия