"""
Trains the fraud detection model and saves it to models/.

Run directly:  python -m app.train_model
Requires:      data/synthetic_events.csv (run app.data_gen first)
"""

import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score

FEATURE_COLUMNS = [
    "amount",
    "known_device",
    "is_foreign_country",
    "is_vpn",
    "login_success",
    "hour_of_day",
]

MODEL_PATH = "models/fraud_model.joblib"


def train():
    data_path = "data/synthetic_events.csv"
    if not os.path.exists(data_path):
        raise FileNotFoundError(
            f"{data_path} not found. Run `python -m app.data_gen` first."
        )

    df = pd.read_csv(data_path)
    X = df[FEATURE_COLUMNS]
    y = df["is_fraud"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        random_state=42,
        class_weight="balanced",
    )
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    probs = clf.predict_proba(X_test)[:, 1]

    print(classification_report(y_test, preds, target_names=["legit", "fraud"]))
    print(f"ROC AUC: {roc_auc_score(y_test, probs):.4f}")

    os.makedirs("models", exist_ok=True)
    joblib.dump({"model": clf, "features": FEATURE_COLUMNS}, MODEL_PATH)
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    train()
