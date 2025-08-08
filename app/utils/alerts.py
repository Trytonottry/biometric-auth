import smtplib
from email.mime.text import MIMEText
from app.config import Config

def send_email_alert(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = Config.ADMIN_EMAIL
    msg['To'] = Config.ADMIN_EMAIL

    try:
        with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
            server.starttls()
            server.login(Config.SMTP_USER, Config.SMTP_PASS)
            server.send_message(msg)
    except Exception as e:
        print(f"Ошибка отправки email: {e}")

def alert_admin(message):
    print(f"[ALERT] {message}")
    send_email_alert("Подозрительная активность", message)