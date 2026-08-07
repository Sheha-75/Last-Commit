"""
Rule-based baseline risk engine.

This mirrors the scoring table from the SentinelShield README exactly.
It exists as a safe, demo-proof fallback that always works even if the
ML model isn't trained yet or misbehaves during the live demo.
"""

from app.schemas import RiskEvent

# Score weights taken directly from the project README
RULE_WEIGHTS = {
    "high_transaction": 30,
    "unknown_device": 15,
    "foreign_country": 20,
    "vpn": 10,
    "failed_login": 15,
    "unusual_time": 10,
}

# Threshold for what counts as a "high value" transaction (tune as needed)
HIGH_TRANSACTION_THRESHOLD = 5000.0

# Incident response bands from the README
def risk_level(score: int) -> str:
    if score >= 86:
        return "Critical"
    if score >= 61:
        return "High"
    if score >= 31:
        return "Medium"
    return "Low"


INCIDENT_ACTION = {
    "Low": "Log Event",
    "Medium": "Notify Customer",
    "High": "Block Transaction",
    "Critical": "Freeze Account & Alert Admin",
}


def rule_based_score(event: RiskEvent) -> dict:
    """Compute a rule-based risk score and list of triggered reasons."""
    reasons = []
    score = 0

    if event.amount is not None and event.amount >= HIGH_TRANSACTION_THRESHOLD:
        score += RULE_WEIGHTS["high_transaction"]
        reasons.append("High Transaction Amount")

    if not event.known_device:
        score += RULE_WEIGHTS["unknown_device"]
        reasons.append("Unknown Device")

    if event.is_foreign_country:
        score += RULE_WEIGHTS["foreign_country"]
        reasons.append("Foreign Country")

    if event.is_vpn:
        score += RULE_WEIGHTS["vpn"]
        reasons.append("VPN")

    if not event.login_success:
        score += RULE_WEIGHTS["failed_login"]
        reasons.append("Failed Login")

    if event.hour_of_day is not None and (event.hour_of_day < 5 or event.hour_of_day > 23):
        score += RULE_WEIGHTS["unusual_time"]
        reasons.append("Unusual Login Time")

    score = min(score, 100)
    level = risk_level(score)

    return {
        "risk_score": score,
        "risk_level": level,
        "recommended_action": INCIDENT_ACTION[level],
        "reasons": reasons,
    }
