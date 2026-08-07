"""
SentinelShield AI - Risk Engine API

Run locally:
    uvicorn app.main:app --reload --port 8000

Endpoints:
    GET  /health              - liveness check
    POST /predict-risk        - score a single login/transaction event
    POST /simulate-attack     - run a preset high-risk scenario through the engine
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import RiskEvent, RiskResponse
from app.risk_rules import rule_based_score
from app.model import get_fraud_model

app = FastAPI(
    title="SentinelShield AI - Risk Engine",
    description="AI-powered fraud risk scoring with explainable AI (SHAP)",
    version="1.0.0",
)

# Allow the React frontend (Vite dev server) to call this API directly.
# Tighten this to your actual frontend origin before deploying.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict-risk", response_model=RiskResponse)
def predict_risk(event: RiskEvent, use_model: bool = True):
    """
    Score a login/transaction event.

    Set use_model=false to force the rule-based baseline (useful if the
    ML model isn't trained yet, or for a guaranteed-stable demo fallback).
    """
    if use_model:
        try:
            model = get_fraud_model()
            result = model.predict(event)
            source = "model"
        except FileNotFoundError:
            # Model not trained yet -> fall back to rules instead of erroring
            result = rule_based_score(event)
            source = "rules"
    else:
        result = rule_based_score(event)
        source = "rules"

    return RiskResponse(user_id=event.user_id, source=source, **result)


# A few preset scenarios for the "Cyber Attack Simulator" feature
ATTACK_SCENARIOS = {
    "high_value_vpn_foreign": RiskEvent(
        user_id="simulated_user",
        amount=9500.0,
        known_device=False,
        is_foreign_country=True,
        is_vpn=True,
        login_success=True,
        hour_of_day=3,
    ),
    "brute_force_login": RiskEvent(
        user_id="simulated_user",
        amount=0.0,
        known_device=False,
        is_foreign_country=False,
        is_vpn=False,
        login_success=False,
        hour_of_day=2,
    ),
    "low_risk_normal": RiskEvent(
        user_id="simulated_user",
        amount=45.0,
        known_device=True,
        is_foreign_country=False,
        is_vpn=False,
        login_success=True,
        hour_of_day=14,
    ),
}


@app.post("/simulate-attack", response_model=RiskResponse)
def simulate_attack(scenario: str = "high_value_vpn_foreign", use_model: bool = True):
    """
    Feed a preset attack scenario through the risk engine, for the
    Admin SOC Dashboard's 'Cyber Attack Simulator' feature.

    Available scenarios: high_value_vpn_foreign, brute_force_login, low_risk_normal
    """
    if scenario not in ATTACK_SCENARIOS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown scenario. Choose from: {list(ATTACK_SCENARIOS.keys())}",
        )
    event = ATTACK_SCENARIOS[scenario]
    return predict_risk(event, use_model=use_model)
