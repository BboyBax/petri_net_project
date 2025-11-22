# tests/test_task3_reachability.py

def test_task3_reachability():
    import os
    import sys
    
    # Add project root
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    from src.task1_parser import parse_pnml
    from src.task3_bdd_computation import symbolic_reachability   

    # Đường dẫn tới PNML
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pnml_path = os.path.join(project_root, 'data', 'pnml', 'example.pnml')

    print("Đọc PNML...")
    petri_net = parse_pnml(pnml_path)

    places       = petri_net["places"]
    transitions  = petri_net["transitions"]
    arcs         = petri_net["arcs"]
    pre_weight   = petri_net["pre_weight"]
    post_weight  = petri_net["post_weight"]
    initial_mark = petri_net["initial_marking"]

    print("Tính reachable markings bằng BDD...")
    bdd, R = symbolic_reachability(
        places,
        transitions,
        arcs,
        pre_weight,
        post_weight,
        initial_mark
    )

    print("Kết quả:")
    print(f"- Số biến BDD: {len(bdd.vars)}")
    print(f"- BDD node count: {bdd.count(R)}")



    # một số assert cơ bản
    assert R is not None
    assert bdd.count(R) > 0

    print("\nTEST 3 PASSED!")


if __name__ == "__main__":
    print("="*60)
    print("CHẠY TEST TASK 3 - BDD REACHABILITY")
    print("="*60)
    try:
        test_task3_reachability()
        print("\n TEST 3 OK!")
    except Exception as e:
        print(f"\n TEST 3 FAILED: {e}")
        import traceback
        traceback.print_exc()
