from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
from app.config import Config

def get_fernet():
    password = Config.ENCRYPTION_KEY.encode()
    salt = b'salt_1234567890'  # В реальности — безопасный солт
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return Fernet(key)

def encrypt_data( bytes) -> bytes:
    f = get_fernet()
    return f.encrypt(data)

def decrypt_file(filepath: str) -> bytes:
    f = get_fernet()
    with open(filepath, 'rb') as f_in:
        encrypted = f_in.read()
    return f.decrypt(encrypted)