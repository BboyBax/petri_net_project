"""
main.py
Điểm bắt đầu của dự án Petri Net
Chủ đề: Symbolic and Algebraic Reasoning in Petri Nets
"""

from src.task1_parser import parse_pnml
from src.task2_graph_construction import build_state_graph
from src.task3_bdd_computation import symbolic_reachability
from src.task4_ilp_formulation import detect_deadlock_ilp
from src.task5_optimize_reachable_markings import maximize_over_markings
from src.utils import print_separator

def main():
    print_separator("START PROJECT: Petri Net Reasoning")

    # 1️⃣ Đọc file PNML
    pnml_file = "data/pnml/example.pnml"
    net = parse_pnml(pnml_file)

    # 2️⃣ Xây dựng đồ thị trạng thái
    graph = build_state_graph(net)

    # 3️⃣ Tính toán BDD từ reachable markings
    bdd = symbolic_reachability(places, transitions, arcs, pre_weight, post_weight, initial_marking)

    # 4️⃣ Kết hợp ILP để phát hiện deadlock (nếu có)
    deadlock = detect_deadlock_ilp(graph, bdd)

    # 5️⃣ Áp dụng symbolic/algebraic reasoning
    maximize_over_markings(graph, bdd, deadlock)

    print_separator("ALL TASKS COMPLETED SUCCESSFULLY ✅")

if __name__ == "__main__":
    main()
