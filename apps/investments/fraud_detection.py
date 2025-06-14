from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import joblib

class FraudDetector:
    """Placeholder machine learning model for fraud detection."""

    def __init__(self, model_path=None):
        if model_path:
            self.model = joblib.load(model_path)
        else:
            self.model = LogisticRegression()

    def train_from_csv(self, csv_path, target_column="Class"):
        """Train the detector from a Kaggle dataset CSV."""
        df = pd.read_csv(csv_path)
        X = df.drop(columns=[target_column])
        y = df[target_column]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        preds = self.model.predict(X_test)
        return accuracy_score(y_test, preds)

    def predict(self, features):
        """Return True if transaction is predicted fraudulent."""
        try:
            result = self.model.predict([features])
            return bool(result[0])
        except Exception:
            return False
