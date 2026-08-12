# Event Engine — Quick Start

## Run it
```bash
cd event-engine
chmod +x test-scenario.sh
./mvnw spring-boot:run
```
(If you don't have the wrapper, use `mvn spring-boot:run` with Maven installed.)

Runs on **http://localhost:8080**

## Test it (in a second terminal, once it's running)
```bash
./test-scenario.sh
```
Should end with `"currentStage": "FRAUD_ATTEMPT"` and `"attackType": "ACCOUNT_TAKEOVER"`.

## Your API contract (give this to Person 2 and Person 4 immediately)

**POST /events** — ingest one signal
```json
{
  "event": "VPN_DETECTED",
  "user": "U001",
  "session": "S123",
  "severity": "MEDIUM"
}
```
Valid `event` values: `NEW_DEVICE`, `VPN_DETECTED`, `UNUSUAL_LOCATION`, `FAILED_LOGIN`,
`SUCCESSFUL_LOGIN`, `PASSWORD_CHANGED`, `NEW_BENEFICIARY`, `HIGH_VALUE_TRANSACTION`

Returns the current `CorrelationResult` (see below) after adding the event.

**GET /sessions/{sessionId}/correlation** — current stage for a session
```json
{
  "session": "S123",
  "currentStage": "FRAUD_ATTEMPT",
  "confidence": 99,
  "matchedEvents": [ ... ],
  "attackType": "ACCOUNT_TAKEOVER"
}
```
`currentStage` is one of: `NORMAL`, `ANOMALY`, `SUSPICIOUS_ACCESS`,
`ACCOUNT_COMPROMISE`, `FINANCIAL_MANIPULATION`, `FRAUD_ATTEMPT`

**GET /sessions/{sessionId}/events** — raw event history (for the Attack Timeline UI)

**DELETE /sessions/{sessionId}** — reset a session (use between demo takes)

## What's next for you
1. Confirm the test scenario passes.
2. Hand the API contract above to Person 2 (they poll `/correlation` to feed the LLM narrative) and Person 4 (their simulator hits `/events` repeatedly).
3. If time allows: tune `computeConfidence()` in `CorrelationEngine.java` and add more nuance to the stage rules (e.g. impossible-travel detection using metadata timestamps/locations).
4. Stop there — don't add persistence, auth, or extra event types unless everything else is done early.
