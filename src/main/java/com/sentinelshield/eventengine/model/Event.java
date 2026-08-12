package com.sentinelshield.eventengine.model;

import java.time.Instant;
import java.util.Map;

public class Event {
    private EventType event;
    private String user;
    private String session;
    private Instant timestamp;
    private String severity; // LOW, MEDIUM, HIGH
    private Map<String, Object> metadata;

    public Event() {
        this.timestamp = Instant.now();
    }

    public EventType getEvent() { return event; }
    public void setEvent(EventType event) { this.event = event; }

    public String getUser() { return user; }
    public void setUser(String user) { this.user = user; }

    public String getSession() { return session; }
    public void setSession(String session) { this.session = session; }

    public Instant getTimestamp() { return timestamp; }
    public void setTimestamp(Instant timestamp) { this.timestamp = timestamp; }

    public String getSeverity() { return severity; }
    public void setSeverity(String severity) { this.severity = severity; }

    public Map<String, Object> getMetadata() { return metadata; }
    public void setMetadata(Map<String, Object> metadata) { this.metadata = metadata; }
}
