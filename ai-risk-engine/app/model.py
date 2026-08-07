"""
Loads the trained fraud model and produces predictions with SHAP-based
human-readable explanations, in the format the README's UI mockup expects
(e.g. "High Transaction Amount", "VPN", "Unknown Device", "Foreign Country").
"""

import os
import joblib
import numpy as np
import pandas as pd
import shap

from app.schemas import RiskEvent
from app.risk_rules import risk_level, INCIDENT_ACTION

MODEL_PATH = "models/fraud_model.joblib"

# Maps raw feature names -> human-readable reason text, and the direction
# of the feature value that counts as "risky" (so we only surface reasons
# that make sense, not just "high SHAP value" for a safe feature).
FEATURE_REASON_MAP = {
    "amount": ("High Transaction Amount", lambda v: v >= 5000),
    "known_device": ("Unknown Device", lambda v: v == 0),
    "is_foreign_country": ("Foreign Country", lambda v: v == 1),
    "is_vpn": ("VPN", lambda v: v == 1),
    "login_success": ("Failed Login", lambda v: v == 0),
    "hour_of_day": ("Unusual Login Time", lambda v: (v < 5) or (v > 23)),
}


class FraudModel:
    def __init__(self, model_path: str = MODEL_PATH):
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"{model_path} not found. Run `python -m app.data_gen` "
                "then `python -m app.train_model` first."
            )
        bundle = joblib.load(model_path)
        self.model = bundle["model"]
        self.features = bundle["features"]
        # TreeExplainer is fast and exact for tree-based models like RandomForest
        self.explainer = shap.TreeExplainer(self.model)

    def _event_to_row(self, event: RiskEvent) -> pd.DataFrame:
        row = {
            "amount": event.amount or 0.0,
            "known_device": int(event.known_device),
            "is_foreign_country": int(event.is_foreign_country),
            "is_vpn": int(event.is_vpn),
            "login_success": int(event.login_success),
            "hour_of_day": event.hour_of_day if event.hour_of_day is not None else 12,
        }
        return pd.DataFrame([row])[self.features]

    def predict(self, event: RiskEvent) -> dict:
        X = self._event_to_row(event)

        fraud_probability = float(self.model.predict_proba(X)[0, 1])
        score = round(fraud_probability * 100)
        level = risk_level(score)

        # SHAP values for the "fraud" class (class index 1).
        # Different shap/sklearn versions return this in different shapes:
        # - list of [n_samples, n_features] arrays, one per class
        # - single array of shape (n_samples, n_features, n_classes)
        # - single array of shape (n_samples, n_features) for binary models
        shap_values = self.explainer.shap_values(X)
        if isinstance(shap_values, list):
            contributions = np.asarray(shap_values[1][0])
        else:
            shap_values = np.asarray(shap_values)
            if shap_values.ndim == 3:
                contributions = shap_values[0, :, 1]  # sample 0, all features, class 1
            else:
                contributions = shap_values[0]

        # Rank features by how much they pushed the prediction toward fraud
        contrib_pairs = list(zip(self.features, contributions))
        contrib_pairs.sort(key=lambda p: p[1], reverse=True)

        reasons = []
        for feature_name, contribution in contrib_pairs:
            if contribution <= 0:
                continue  # only surface features that increased risk
            label, is_risky = FEATURE_REASON_MAP[feature_name]
            value = X.iloc[0][feature_name]
            if is_risky(value):
                reasons.append(label)

        return {
            "risk_score": score,
            "risk_level": level,
            "recommended_action": INCIDENT_ACTION[level],
            "reasons": reasons,
            "fraud_probability": round(fraud_probability, 4),
        }


# Singleton, loaded lazily so the API can start even before training
_fraud_model_instance = None


def get_fraud_model() -> "FraudModel":
    global _fraud_model_instance
    if _fraud_model_instance is None:
        _fraud_model_instance = FraudModel()
    return _fraud_model_instance
