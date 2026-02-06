"""Simple in-memory telemetry shim for tests."""
_events = []

def emit(name, payload=None):
    _events.append({"name": name, "payload": payload})

def events():
    return list(_events)

def clear():
    _events.clear()

# minimal helper for tests
def last():
    return _events[-1] if _events else None
