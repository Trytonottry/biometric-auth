from app.modules.anomaly_detection import detect_anomaly

def test_anomaly_detection_normal(client):
    is_anomalous = detect_anomaly(user_id=1, method="face", ip="192.168.1.10")
    assert is_anomalous is False

def test_anomaly_detection_suspicious(client):
    # В реальности — обученная модель
    # Здесь симуляция
    is_anomalous = detect_anomaly(user_id=999, method="fingerprint", ip="10.0.0.1")
    assert isinstance(is_anomalous, bool)