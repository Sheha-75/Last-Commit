package com.sentinelshield.eventengine.controller;

import com.sentinelshield.eventengine.model.CorrelationResult;
import com.sentinelshield.eventengine.model.Event;
import com.sentinelshield.eventengine.service.CorrelationEngine;
import com.sentinelshield.eventengine.service.EventStore;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@CrossOrigin(origins = "*") // fine for a hackathon demo; tighten later if needed
public class EventController {

    private final EventStore eventStore;
    private final CorrelationEngine correlationEngine;

    public EventController(EventStore eventStore, CorrelationEngine correlationEngine) {
        this.eventStore = eventStore;
        this.correlationEngine = correlationEngine;
    }

    // Ingest a single signal. Person 4's simulator calls this repeatedly to replay an attack.
    @PostMapping("/events")
    public CorrelationResult ingestEvent(@RequestBody Event event) {
        eventStore.addEvent(event);
        List<Event> sessionEvents = eventStore.getEvents(event.getSession());
        return correlationEngine.correlate(event.getSession(), sessionEvents);
    }

    // Read the current correlation state for a session. Person 2 (AI) and
    // Person 1 (dashboard) both call this.
    @GetMapping("/sessions/{sessionId}/correlation")
    public CorrelationResult getCorrelation(@PathVariable String sessionId) {
        List<Event> sessionEvents = eventStore.getEvents(sessionId);
        return correlationEngine.correlate(sessionId, sessionEvents);
    }

    // Raw event history for the Attack Timeline UI component.
    @GetMapping("/sessions/{sessionId}/events")
    public List<Event> getEvents(@PathVariable String sessionId) {
        return eventStore.getEvents(sessionId);
    }

    // Reset a session between simulator runs/demo takes.
    @DeleteMapping("/sessions/{sessionId}")
    public void clearSession(@PathVariable String sessionId) {
        eventStore.clearSession(sessionId);
    }
}
