def test_parse_pnml_exists():
    from src.task1_parser import parse_pnml
    result = parse_pnml('data/pnml/example.pnml')
    assert isinstance(result, dict)
    assert 'places' in result and 'transitions' in result and 'arcs' in result
