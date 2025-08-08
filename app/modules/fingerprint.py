import hashlib

def capture_fingerprint():
    # Симуляция: в реальности — драйвер сенсора
    raw_data = "fingerprint_sensor_data_" + str(hash("temp"))
    return hashlib.sha256(raw_data.encode()).hexdigest()

def verify_fingerprint(user, provided_hash):
    return user.fingerprint_hash == provided_hash