package com.sentinelshield.eventengine.model;

import java.util.List;

public class CorrelationResult {
    private String session;
    private AttackStage currentStage;
    private int confidence; // 0-100
    private List<Event> matchedEvents;
    private String attackType; // e.g. "ACCOUNT_TAKEOVER" or "NONE"

    public CorrelationResult(String session, AttackStage currentStage, int confidence,
                              List<Event> matchedEvents, String attackType) {
        this.session = session;
        this.currentStage = currentStage;
        this.confidence = confidence;
        this.matchedEvents = matchedEvents;
        this.attackType = attackType;
    }

    public String getSession() { return session; }
    public AttackStage getCurrentStage() { return currentStage; }
    public int getConfidence() { return confidence; }
    public List<Event> getMatchedEvents() { return matchedEvents; }
    public String getAttackType() { return attackType; }
}
