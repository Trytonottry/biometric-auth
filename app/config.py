import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-biometric-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///biometric.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BIOMETRIC_STORAGE = os.path.join(os.getcwd(), 'data', 'biometric_templates')
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY') or 'AES256_KEY_32_CHARSssssssssssssss'