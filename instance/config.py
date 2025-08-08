# instance/config.py

import os

# Генерация: os.urandom(24).hex()
SECRET_KEY = 'your_flask_secret_key_here_123456'

# База данных
SQLALCHEMY_DATABASE_URI = 'sqlite:///biometric.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Шифрование биометрических данных
ENCRYPTION_KEY = 'thisis32charlongencryptionkey!!!'  # 32 символа

# Путь к хранилищу шаблонов
BIOMETRIC_STORAGE = os.path.join(os.getcwd(), 'data', 'biometric_templates')

# Режим (production / development)
ENV = 'development'

# Настройки безопасности
MAX_LOGIN_ATTEMPTS = 5
BLOCK_DURATION_MINUTES = 15

ADMIN_EMAIL = 'admin@company.com'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'your_email@gmail.com'
SMTP_PASS = 'your_app_password'

# LDAP / Active Directory
LDAP_SERVER = 'ldap://your-domain-controller.com'
LDAP_DOMAIN = 'YOURDOMAIN'

# Поведенческая биометрия
BEHAVIORAL_ENABLED = True