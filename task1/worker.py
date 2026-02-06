import time
from . import telemetry


def run(request: dict) -> dict:
    start = time.time()
    task_id = request.get("id", "unknown")
    telemetry.emit("task1.started", {"task_id": task_id, "payload_size": len(str(request.get("payload", {})))})

    # Minimal deterministic processing
    output = request.get("payload", {})
    result = {"id": task_id, "status": "ok", "output": output}

    duration_ms = int((time.time() - start) * 1000)
    telemetry.emit("task1.completed", {"task_id": task_id, "duration_ms": duration_ms})
    return result
