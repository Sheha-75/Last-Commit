#!/bin/bash
# Replays the reference account-takeover scenario against the running Event Engine.
# Run: ./test-scenario.sh   (make sure the app is running on localhost:8080 first)

BASE_URL="http://localhost:8080"
SESSION="S123"
USER="U001"

post_event() {
  local event=$1
  local severity=$2
  echo "-> $event"
  curl -s -X POST "$BASE_URL/events" \
    -H "Content-Type: application/json" \
    -d "{\"event\":\"$event\",\"user\":\"$USER\",\"session\":\"$SESSION\",\"severity\":\"$severity\"}" \
    | python3 -m json.tool
  echo ""
}

echo "=== Resetting session ==="
curl -s -X DELETE "$BASE_URL/sessions/$SESSION"
echo ""

echo "=== Replaying attack sequence ==="
post_event "NEW_DEVICE" "MEDIUM"
post_event "VPN_DETECTED" "MEDIUM"
post_event "FAILED_LOGIN" "MEDIUM"
post_event "FAILED_LOGIN" "MEDIUM"
post_event "SUCCESSFUL_LOGIN" "LOW"
post_event "PASSWORD_CHANGED" "HIGH"
post_event "NEW_BENEFICIARY" "HIGH"
post_event "HIGH_VALUE_TRANSACTION" "HIGH"

echo "=== Final correlation state (should be FRAUD_ATTEMPT) ==="
curl -s "$BASE_URL/sessions/$SESSION/correlation" | python3 -m json.tool
