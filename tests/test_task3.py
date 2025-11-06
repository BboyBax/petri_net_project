def test_compute_bdd_signature():
    from src.task3_bdd_computation import compute_bdd
    b = compute_bdd({})
    assert isinstance(b, dict)
