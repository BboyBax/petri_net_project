def test_perform_symbolic_reasoning_runs():
    from src.task5_symbolic_reasoning import perform_symbolic_reasoning
    r = perform_symbolic_reasoning({}, {}, False)
    assert r is None
