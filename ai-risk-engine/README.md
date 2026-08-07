# SentinelShield AI - Risk Engine

The Python/ML component of SentinelShield AI: a fraud risk-scoring service
with a rule-based baseline, a trained Random Forest model, and SHAP-based
explainability.

## Project layout

```
ai-risk-engine/
├── app/
│   ├── main.py          # FastAPI app (the API you run)
│   ├── schemas.py        # Request/response models
│   ├── risk_rules.py      # Rule-based baseline scorer (always works)
│   ├── data_gen.py         # Generates synthetic training data
│   ├── train_model.py       # Trains the Random Forest model
│   └── model.py               # Loads model + produces SHAP explanations
├── data/                # Created by data_gen.py (gitignored)
├── models/              # Created by train_model.py (gitignored)
├── requirements.txt
├── Dockerfile
└── README.md
```

## Setup in VS Code

1. **Open the folder.** File → Open Folder → select `ai-risk-engine`.

2. **Install the Python extension** if you don't have it (search "Python" by
   Microsoft in the Extensions panel, `Ctrl+Shift+X`).

3. **Create a virtual environment.** Open a terminal in VS Code
   (`` Ctrl+` ``) and run:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # on Windows: .venv\Scripts\activate
   ```
   VS Code should prompt you to select this as your workspace interpreter —
   click "Yes". If not, use `Ctrl+Shift+P` → "Python: Select Interpreter" →
   pick the one inside `.venv`.

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Generate the synthetic dataset:**
   ```bash
   python -m app.data_gen
   ```
   This writes `data/synthetic_events.csv`. Check the printed fraud rate —
   it should be roughly 8-15%.

6. **Train the model:**
   ```bash
   python -m app.train_model
   ```
   This prints a classification report and saves `models/fraud_model.joblib`.
   Don't worry if precision/recall on the "fraud" class looks unimpressive —
   that's expected with synthetic data; what matters for the demo is that
   individual predictions and their SHAP explanations look sensible.

7. **Run the API:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   Then open **http://localhost:8000/docs** in a browser — FastAPI
   auto-generates an interactive Swagger UI where you can try every endpoint
   without writing any curl commands. This is the fastest way to sanity-check
   your work and to show your teammates what the API looks like.

## Testing it

In the Swagger UI (`/docs`), try `POST /predict-risk` with something like:
```json
{
  "user_id": "user_123",
  "amount": 8500,
  "known_device": false,
  "is_foreign_country": true,
  "is_vpn": true,
  "login_success": true,
  "hour_of_day": 3
}
```
You should get back a risk score, a risk level (Low/Medium/High/Critical),
a recommended action, and a list of plain-English reasons — this is the
"Explainable AI" piece from the project README.

Try `POST /simulate-attack?scenario=high_value_vpn_foreign` (or
`brute_force_login`, `low_risk_normal`) to power the Cyber Attack Simulator
feature on the Admin dashboard.

If you ever want to bypass the ML model and use the guaranteed-stable
rule-based scorer instead (handy right before a demo), call
`POST /predict-risk?use_model=false`.

## Integrating with the rest of the team

- Share the `/docs` URL with whoever's building the Spring Boot backend or
  the React frontend so they can see the exact request/response shape.
- If the backend team wants your service behind their API instead of
  calling it directly, they can proxy requests to
  `http://localhost:8000/predict-risk` from Spring Boot.
- To run this alongside the rest of the stack without dependency clashes,
  build and run the Docker image:
  ```bash
  docker build -t sentinelshield-risk-engine .
  docker run -p 8000:8000 sentinelshield-risk-engine
  ```

## Next steps / stretch goals

- Swap the synthetic dataset for a public fraud dataset (e.g. Kaggle's
  "Credit Card Fraud Detection") if you have time, for a more convincing
  ROC AUC.
- Try an Isolation Forest as a second model and compare — it doesn't need
  labels, which is a nice talking point for "detecting unseen fraud
  patterns" in your pitch.
- Add a `/retrain` endpoint so the Admin dashboard could trigger retraining
  live during the demo (impressive, but only worth it if you have spare time).
