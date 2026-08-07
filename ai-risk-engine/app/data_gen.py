"""
Generates a synthetic dataset of login/transaction events for training.

Run directly:  python -m app.data_gen
Produces:       data/synthetic_events.csv
"""

import numpy as np
import pandas as pd
import os

RNG_SEED = 42
N_ROWS = 6000


def generate_dataset(n_rows: int = N_ROWS, seed: int = RNG_SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    amount = rng.exponential(scale=800, size=n_rows).round(2)
    known_device = rng.random(n_rows) > 0.25
    is_foreign_country = rng.random(n_rows) > 0.85
    is_vpn = rng.random(n_rows) > 0.9
    login_success = rng.random(n_rows) > 0.1
    hour_of_day = rng.integers(0, 24, size=n_rows)

    df = pd.DataFrame(
        {
            "amount": amount,
            "known_device": known_device.astype(int),
            "is_foreign_country": is_foreign_country.astype(int),
            "is_vpn": is_vpn.astype(int),
            "login_success": login_success.astype(int),
            "hour_of_day": hour_of_day,
        }
    )

    # Derive a rule-based severity score (same weights as risk_rules.py)
    score = (
        (df["amount"] >= 5000).astype(int) * 30
        + (1 - df["known_device"]) * 15
        + df["is_foreign_country"] * 20
        + df["is_vpn"] * 10
        + (1 - df["login_success"]) * 15
        + ((df["hour_of_day"] < 5) | (df["hour_of_day"] > 23)).astype(int) * 10
    )

    # Label as fraud when score is high, plus a little random noise so the
    # model has to learn patterns rather than just memorizing the rule.
    # Center/scale tuned so fraud sits around ~12-15% of events -- enough
    # signal for the model to learn from in a small synthetic dataset,
    # while still being clearly the minority class.
    prob_fraud = 1 / (1 + np.exp(-(score - 40) / 10))
    noise = rng.random(n_rows)
    df["is_fraud"] = (noise < prob_fraud).astype(int)

    return df


if __name__ == "__main__":
    df = generate_dataset()
    os.makedirs("data", exist_ok=True)
    out_path = "data/synthetic_events.csv"
    df.to_csv(out_path, index=False)
    print(f"Wrote {len(df)} rows to {out_path}")
    print(f"Fraud rate: {df['is_fraud'].mean():.2%}")
