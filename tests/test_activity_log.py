from studio.activity_log import ACTIVITY_EVENT, MAX_ENTRIES, ActivityLog
from studio.events import EventBus


def test_activity_log_starts_empty():
    log = ActivityLog(EventBus())

    assert log.entries == []


def test_activity_log_records_a_published_message():
    events = EventBus()
    log = ActivityLog(events)

    events.publish(ACTIVITY_EVENT, {"message": "Tablero añadido: B1"})

    assert len(log.entries) == 1
    assert "Tablero añadido: B1" in log.entries[0]


def test_activity_log_shows_newest_entry_first():
    events = EventBus()
    log = ActivityLog(events)

    events.publish(ACTIVITY_EVENT, {"message": "primero"})
    events.publish(ACTIVITY_EVENT, {"message": "segundo"})

    assert "segundo" in log.entries[0]
    assert "primero" in log.entries[1]


def test_activity_log_ignores_unrelated_events():
    events = EventBus()
    log = ActivityLog(events)

    events.publish("otro.evento", {"message": "no debería aparecer"})

    assert log.entries == []


def test_activity_log_caps_at_max_entries():
    events = EventBus()
    log = ActivityLog(events)

    for i in range(MAX_ENTRIES + 10):
        events.publish(ACTIVITY_EVENT, {"message": f"evento {i}"})

    assert len(log.entries) == MAX_ENTRIES
    assert f"evento {MAX_ENTRIES + 9}" in log.entries[0]
