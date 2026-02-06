def test_run_returns_expected_structure():
    from task1.worker import run
    req = {"id": "t1", "payload": {"a": 1}}
    res = run(req)
    assert isinstance(res, dict)
    assert res["status"] == "ok"
    assert "output" in res
