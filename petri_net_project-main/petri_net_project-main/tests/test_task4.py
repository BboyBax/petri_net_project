def test_detect_deadlock_ilp_signature():
    from src.task4_ilp_formulation import detect_deadlock_ilp
    d = detect_deadlock_ilp({}, {})
    assert d in (True, False, None)
