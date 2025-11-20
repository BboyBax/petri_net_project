def test_build_state_graph_signature():
    from src.task2_graph_construction import build_state_graph
    g = build_state_graph({})
    assert isinstance(g, dict)
