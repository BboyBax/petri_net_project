def test_parse_pnml_exists():
    import os
    import sys
    # add project root (parent of tests/) so `src` package is importable
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from src.task1_parser import parse_pnml
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pnml_path = os.path.join(project_root, 'data', 'pnml', 'phylosopher.pnml')
    
    result = parse_pnml(pnml_path)
    assert isinstance(result, dict)
    assert 'places' in result and 'transitions' in result and 'arcs' in result

if __name__ == "__main__":
    print("="*60)
    print("🧪 CHẠY TEST")
    print("="*60)
    try:
        test_parse_pnml_exists()
        print("\n✅✅✅ TEST PASSED - CODE ĐÚNG!")
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
