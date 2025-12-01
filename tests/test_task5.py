import numpy as np
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.task5_optimize_reachable_markings import max_reachable_marking
from src.task4_deadlock_detection import deadlock_reachable_marking
from src.task1_parser import PetriNet
from src.task3_symbolic_reachability import bdd_reachable, compare_methods, print_all_markings_bdd
from src.task2_explicit_reachability import explicit_reachability, print_all_markings
from pyeda.inter import *
from pathlib import Path

def test_001():
    # Đường dẫn tới file PNML bạn muốn test (ví dụ OptTestNet.pnml)
    base_dir = Path(__file__).parent.parent / "data" / "pnml"
    pn = PetriNet.from_pnml(str(base_dir / "optimization1.pnml"))
    errors = pn.validate()
    if errors:
        print("Validation errors found:")
        for e in errors:
            print(" -", e)
    else:
        # Tính reachable markings bằng BDD
        bdd, R = bdd_reachable(pn)

        # Vector trọng số c (ví dụ: ưu tiên p3 và p4)
        c = np.array([0, 2, 5, 3])   # độ dài bằng số place

        # Gọi hàm tối ưu
        marking, value = max_reachable_marking(pn.place_ids, R, c)

        # In ra để kiểm tra
        print("Optimal marking:", marking)
        print("Optimal value:", value)

        # Ví dụ assert: nếu bạn biết trước kết quả mong đợi
        assert value == max(np.dot(c, m) for m in explicit_reachability(pn))
    

def test_002():
    # Đọc file PNML
    base_dir = Path(__file__).parent.parent / "data" / "pnml"
    pn = PetriNet.from_pnml(str(base_dir / "optimization2.pnml"))
    errors = pn.validate()
    if errors:
        print("Validation errors found:")
        for e in errors:
            print(" -", e)
    else:
        # Tính reachable markings bằng BDD
        bdd, R = bdd_reachable(pn)

        # Vector trọng số c (ví dụ: ưu tiên p5 cao nhất)
        c = np.array([0, 1, 2, 2, 5])  # độ dài bằng số place

        # Gọi hàm tối ưu
        marking, value = max_reachable_marking(pn.place_ids, R, c)

        print("Optimal marking:", marking)
        print("Optimal value:", value)

        # Kiểm tra: giá trị tối ưu phải bằng max(c⊤M) trên tập reachable
        # Ta có thể so sánh với explicit_reachability nếu muốn chắc chắn
        reachable = explicit_reachability(pn)
        max_val = max(np.dot(c, m) for m in reachable)
        assert value == max_val

def test_003():
    # Đọc file PNML
    base_dir = Path(__file__).parent.parent / "data" / "pnml"
    pn = PetriNet.from_pnml(str(base_dir / "optimization3.pnml"))
    errors = pn.validate()
    if errors:
        print("Validation errors found:")
        for e in errors:
            print(" -", e)
    else:
        # Tính reachable bằng BDD
        bdd, R = bdd_reachable(pn)

        # Vector trọng số
        # c = np.array([0, 1, 2, 2, 3, 3, 4, 4, 5, 10])
        c = np.array([0, 0, 2, 2, 3, 3, 4, 4, 12, 10])

        # Tìm marking tối ưu
        marking, value = max_reachable_marking(pn.place_ids, R, c)
        print("Optimal marking:", marking)
        print("Optimal value:", value)

        # So sánh với explicit để chắc chắn
        reachable = explicit_reachability(pn)
        max_val = max(np.dot(c, m) for m in reachable)
        assert value == max_val
