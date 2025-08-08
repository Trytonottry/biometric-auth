import os
from app.config import Config

def save_biometric_data(data: bytes, username: str, filename: str):
    user_dir = os.path.join(Config.BIOMETRIC_STORAGE, username)
    os.makedirs(user_dir, exist_ok=True)
    path = os.path.join(user_dir, filename)
    with open(path, 'wb') as f:
        f.write(data)
    return path