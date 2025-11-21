def test_build_state_graph_signature():
    import os
    import sys
    # Add project root
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    from src.task1_parser import parse_pnml
    from src.task2_graph_construction import build_state_graph
    
    # Đường dẫn đến file phylosopher.pnml
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pnml_path = os.path.join(project_root, 'data', 'pnml', 'phylosopher.pnml')
    
    # Parse PNML
    print("📖 Đọc file phylosopher.pnml...")
    petri_net = parse_pnml(pnml_path)
    
    print(f"✓ Số places: {len(petri_net['places'])}")
    print(f"✓ Số transitions: {len(petri_net['transitions'])}")
    print(f"✓ Số arcs: {len(petri_net['arcs'])}")
    
    # Build state graph
    print("\n🔨 Xây dựng state graph...")
    g = build_state_graph(petri_net)
    
    # Assertions
    assert isinstance(g, dict)
    assert 'nodes' in g
    assert 'edges' in g
    assert 'initial_marking' in g
    
    print(f"\n✅ State graph built successfully!")
    print(f"   - Số states: {len(g['nodes'])}")
    print(f"   - Số transitions: {len(g['edges'])}")

if __name__ == "__main__":
    print("="*60)
    print("🧪 CHẠY TEST TASK 2 - PHYLOSOPHER")
    print("="*60)
    try:
        test_build_state_graph_signature()
        print("\n✅✅✅ TEST PASSED - CODE ĐÚNG!")
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()