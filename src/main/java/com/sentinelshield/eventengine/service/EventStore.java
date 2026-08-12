package com.sentinelshield.eventengine.service;

import com.sentinelshield.eventengine.model.Event;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;

@Component
public class EventStore {

    // session_id -> ordered list of events (thread-safe, in-memory, no DB needed today)
    private final Map<String, List<Event>> sessions = new ConcurrentHashMap<>();

    public void addEvent(Event event) {
        sessions
            .computeIfAbsent(event.getSession(), id -> new CopyOnWriteArrayList<>())
            .add(event);
    }

    public List<Event> getEvents(String sessionId) {
        return sessions.getOrDefault(sessionId, List.of());
    }

    public void clearSession(String sessionId) {
        sessions.remove(sessionId);
    }
}
