# Симуляция распознавания радужки
import hashlib
import random

def capture_iris():
    # Имитация данных радужки
    return hashlib.sha256(f"iris_{random.random()}".encode()).hexdigest()

def verify_iris(user, captured_hash):
    stored = user.iris_template
    return stored and stored == captured_hash