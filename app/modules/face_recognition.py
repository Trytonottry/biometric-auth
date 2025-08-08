import cv2
import face_recognition
import os
from app.utils.encryption import decrypt_file, encrypt_data
import numpy as np

def capture_face():
    cap = cv2.VideoCapture(0)
    print("Сделайте фото (нажмите 'q' для сохранения)")
    while True:
        ret, frame = cap.read()
        cv2.imshow('Face Capture', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

    # Получаем вектор признаков лица
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(rgb_frame)
    return encodings[0].tobytes() if encodings else None

def verify_face(user, live_encoding_bytes):
    if not user.face_template:
        return False

    try:
        decrypted = decrypt_file(user.face_template)
        stored_encoding = np.frombuffer(decrypted, dtype=np.float64)
        live_encoding = np.frombuffer(live_encoding_bytes, dtype=np.float64)

        # Сравнение
        matches = face_recognition.compare_faces([stored_encoding], live_encoding, tolerance=0.6)
        return matches[0]
    except Exception as e:
        print(f"Ошибка при сравнении лиц: {e}")
        return False