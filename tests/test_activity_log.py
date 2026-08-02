from studio.activity_log import ACTIVITY_EVENT, MAX_ENTRIES, ActivityLog
from studio.events import EventBus


def test_activity_log_starts_empty():
    log = ActivityLog(EventBus())

    assert log.entries == []


def test_activity_log_records_a_published_message():
    events = EventBus()
    log = ActivityLog(events)

    events.publish(ACTIVITY_EVENT, {"message": "Tablero añadido: B1", "category": "tablero"})

    assert len(log.entries) == 1
    assert log.entries[0].message == "Tablero añadido: B1"
    assert log.entries[0].category == "tablero"


def test_activity_log_shows_newest_entry_first():
    events = EventBus()
    log = ActivityLog(events)

    events.publish(ACTIVITY_EVENT, {"message": "primero", "category": "proyecto"})
    events.publish(ACTIVITY_EVENT, {"message": "segundo", "category": "proyecto"})

    assert log.entries[0].message == "segundo"
    assert log.entries[1].message == "primero"


def test_activity_log_ignores_unrelated_events():
    events = EventBus()
    log = ActivityLog(events)

    events.publish("otro.evento", {"message": "no debería aparecer"})

    assert log.entries == []


def test_activity_log_caps_at_max_entries():
    events = EventBus()
    log = ActivityLog(events)

    for i in range(MAX_ENTRIES + 10):
        events.publish(ACTIVITY_EVENT, {"message": f"evento {i}", "category": "proyecto"})

    assert len(log.entries) == MAX_ENTRIES
    assert log.entries[0].message == f"evento {MAX_ENTRIES + 9}"
