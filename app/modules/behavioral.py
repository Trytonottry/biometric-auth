import numpy as np
from sklearn.ensemble import IsolationForest
from app.models import UserInteractionLog  # новая модель

# Пример признаков: [время_ввода, паузы, скорость_движения, угол_мыши]
FEATURE_NAMES = ['typing_speed', 'mouse_speed', 'click_pattern', 'session_duration']

class BehavioralAuth:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)

    def extract_features(self, interactions):
        if len(interactions) < 5:
            return np.zeros((1, 4))

        typing = np.mean([i.duration for i in interactions if i.event == 'keypress'])
        mouse = np.mean([i.speed for i in interactions if i.event == 'mousemove'])
        clicks = len([i for i in interactions if i.event == 'click'])
        duration = (interactions[-1].timestamp - interactions[0].timestamp).total_seconds()

        return np.array([[typing, mouse, clicks, duration]])

    def train(self, user_id):
        from app.models import UserInteractionLog
        logs = UserInteractionLog.query.filter_by(user_id=user_id).all()
        if len(logs) < 10:
            return False

        X = self.extract_features(logs)
        self.model.fit(X)
        return True

    def is_anomalous(self, user_id, current_interactions):
        X = self.extract_features(current_interactions)
        pred = self.model.predict(X)
        return pred[0] == -1  # -1 = аномалия