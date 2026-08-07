from pydantic import BaseModel, Field
from typing import Optional, List


class RiskEvent(BaseModel):
    """A single login or transaction event to be scored."""

    user_id: str = Field(..., description="ID of the user/account")
    amount: Optional[float] = Field(0.0, description="Transaction amount, 0 for pure logins")
    known_device: bool = Field(True, description="Whether this device has been seen before")
    is_foreign_country: bool = Field(False, description="Login/transaction from unusual country")
    is_vpn: bool = Field(False, description="Whether a VPN/proxy was detected")
    login_success: bool = Field(True, description="Whether the login attempt succeeded")
    hour_of_day: Optional[int] = Field(12, ge=0, le=23, description="Hour of day (0-23) of the event")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "amount": 8500.0,
                "known_device": False,
                "is_foreign_country": True,
                "is_vpn": True,
                "login_success": True,
                "hour_of_day": 3,
            }
        }


class RiskResponse(BaseModel):
    user_id: str
    risk_score: float
    risk_level: str
    recommended_action: str
    reasons: List[str]
    source: str  # "rules" or "model"
    fraud_probability: Optional[float] = None
