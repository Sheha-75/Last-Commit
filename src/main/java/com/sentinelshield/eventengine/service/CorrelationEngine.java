package com.sentinelshield.eventengine.service;

import com.sentinelshield.eventengine.model.AttackStage;
import com.sentinelshield.eventengine.model.CorrelationResult;
import com.sentinelshield.eventengine.model.Event;
import com.sentinelshield.eventengine.model.EventType;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

@Component
public class CorrelationEngine {

    /**
     * Rule-based stage detection. No ML training needed - this is a deliberate
     * scope decision so the whole thing is buildable in a day. Each stage check
     * looks at what event TYPES are present in the session so far.
     */
    public CorrelationResult correlate(String sessionId, List<Event> events) {
        Set<EventType> present = events.stream()
                .map(Event::getEvent)
                .collect(Collectors.toSet());

        long failedLogins = events.stream()
                .filter(e -> e.getEvent() == EventType.FAILED_LOGIN)
                .count();

        AttackStage stage = AttackStage.NORMAL;
        String attackType = "NONE";

        // Stage 5 - Fraud Attempt
        if (present.contains(EventType.HIGH_VALUE_TRANSACTION)
                && present.contains(EventType.NEW_BENEFICIARY)) {
            stage = AttackStage.FRAUD_ATTEMPT;
            attackType = "ACCOUNT_TAKEOVER";
        }
        // Stage 4 - Financial Manipulation
        else if (present.contains(EventType.NEW_BENEFICIARY)
                && (present.contains(EventType.PASSWORD_CHANGED) || present.contains(EventType.SUCCESSFUL_LOGIN))) {
            stage = AttackStage.FINANCIAL_MANIPULATION;
            attackType = "ACCOUNT_TAKEOVER";
        }
        // Stage 3 - Account Compromise
        else if (present.contains(EventType.PASSWORD_CHANGED)
                || (present.contains(EventType.SUCCESSFUL_LOGIN) && failedLogins > 0)) {
            stage = AttackStage.ACCOUNT_COMPROMISE;
            attackType = "ACCOUNT_TAKEOVER";
        }
        // Stage 2 - Suspicious Access
        else if (present.contains(EventType.VPN_DETECTED) || failedLogins >= 2) {
            stage = AttackStage.SUSPICIOUS_ACCESS;
            attackType = "SUSPICIOUS_LOGIN";
        }
        // Stage 1 - Anomaly
        else if (present.contains(EventType.NEW_DEVICE) || present.contains(EventType.UNUSUAL_LOCATION)) {
            stage = AttackStage.ANOMALY;
            attackType = "ANOMALY";
        }

        int confidence = computeConfidence(stage, present.size());

        return new CorrelationResult(sessionId, stage, confidence, events, attackType);
    }

    private int computeConfidence(AttackStage stage, int distinctEventCount) {
        int base = switch (stage) {
            case NORMAL -> 0;
            case ANOMALY -> 40;
            case SUSPICIOUS_ACCESS -> 60;
            case ACCOUNT_COMPROMISE -> 75;
            case FINANCIAL_MANIPULATION -> 85;
            case FRAUD_ATTEMPT -> 95;
        };
        // small bump per corroborating distinct event, capped at 99
        int boosted = base + Math.min(distinctEventCount * 2, 10);
        return Math.min(boosted, 99);
    }
}
