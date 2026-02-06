def test_telemetry_events_emitted():
    from task1 import telemetry
    from task1.worker import run

    telemetry.clear()
    req = {"id": "t2", "payload": {}}
    _ = run(req)
    events = telemetry.events()
    names = [e["name"] for e in events]
    assert "task1.started" in names
    assert "task1.completed" in names
