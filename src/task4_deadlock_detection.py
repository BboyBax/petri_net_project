# """ 
# Task 4 - Thành viên 4
# Phát hiện deadlock bằng cách kết hợp ILP và BDD.
# """

# import collections
# from typing import Tuple, List, Optional
# from pyeda.inter import *
# from collections import deque
# import sys, os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from src.task1_parser import PetriNet
# import numpy as np
# import pulp

# def find_deadlock_candidates_ilp(       
#     pn: PetriNet,  
# ) -> List[List[int]]:
#     num_places = len(pn.place_ids)
#     num_transitions = pn.I.shape[0]

#     # Biến ILP: m_p cho mỗi place
#     m_vars = [pulp.LpVariable(f"m_{i}", lowBound=0, upBound=1, cat="Integer") 
#               for i in range(num_places)]
#     sigma_vars = [pulp.LpVariable(f"sigma_{t}", lowBound=0, upBound=1, cat="Integer") 
#                   for t in range(num_transitions)]

#     # Mô hình ILP
#     model = pulp.LpProblem("DeadlockDetection", pulp.LpMinimize)

#     # 1. Phương trình trạng thái: m = M0 + C * sigma
#     C = pn.O - pn.I
#     for p in range(num_places):
#         model += m_vars[p] == pn.M0[p] + pulp.lpSum(C[t, p] * sigma_vars[t] for t in range(num_transitions))

#     # 2. Deadlock constraints: mọi transition đều không khả dụng
#     for t in range(num_transitions):
#         expr = []
#         for p in range(num_places):
#             is_input = (pn.I[t, p] == 1)
#             is_output = (pn.O[t, p] == 1)
#             if is_input:
#                 expr.append(1 - m_vars[p])  # input thiếu token
#             if is_output and not is_input:
#                 expr.append(m_vars[p])      # output đã có token
#         # Ít nhất một điều kiện vi phạm
#         model += pulp.lpSum(expr) >= 1

#     # Không cần tối ưu, chỉ cần nghiệm khả thi
#     model.solve(pulp.PULP_CBC_CMD(msg=0))

#     if pulp.LpStatus[model.status] != "Optimal":
#         return []

#     # Trích xuất marking ứng viên
#     candidate = [int(pulp.value(m_vars[p])) for p in range(num_places)]
#     return [candidate]

# def validate_deadlocks_with_bdd(pn, bdd, candidates):
#     places = pn.place_ids
#     vars_map = {pid: bddvar(pid) for pid in places}
#     confirmed = []

#     for m in candidates:
#         # Encode marking thành BDD
#         m_bdd = 1
#         for val, pid in zip(m, places):
#             if val == 1:
#                 m_bdd &= vars_map[pid]
#             else:
#                 m_bdd &= ~vars_map[pid]

#         # Kiểm tra xem marking có nằm trong reachable set không
#         if (bdd & m_bdd).satisfy_one() is not None:
#             confirmed.append(m)

#     return confirmed


# def deadlock_reachable_marking( 
#     pn: PetriNet, 
#     bdd: BinaryDecisionDiagram, 
# ) -> Optional[List[int]]:
#     """
#     Kết hợp ILP và BDD để phát hiện deadlock.
#     """
#     candidates = find_deadlock_candidates_ilp(pn)
#     confirmed = validate_deadlocks_with_bdd(pn, bdd, candidates)
#     if not confirmed:  
#         return None
#     return confirmed[0]

"""
Task 4 - Thành viên 4
Phát hiện deadlock bằng cách kết hợp ILP và BDD.
"""

import pulp
from typing import List, Optional
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.task1_parser import PetriNet
from dd.autoref import BDD

def find_deadlock_candidates_ilp(pn: PetriNet) -> List[List[int]]:
    num_places = len(pn.place_ids)
    num_transitions = pn.I.shape[0]

    # Biến ILP: m_p cho mỗi place
    m_vars = [pulp.LpVariable(f"m_{i}", lowBound=0, upBound=1, cat="Integer") 
              for i in range(num_places)]
    sigma_vars = [pulp.LpVariable(f"sigma_{t}", lowBound=0, upBound=1, cat="Integer") 
                  for t in range(num_transitions)]

    # Mô hình ILP
    model = pulp.LpProblem("DeadlockDetection", pulp.LpMinimize)

    # 1. Phương trình trạng thái: m = M0 + C * sigma
    C = pn.O - pn.I
    for p in range(num_places):
        model += m_vars[p] == pn.M0[p] + pulp.lpSum(C[t, p] * sigma_vars[t] for t in range(num_transitions))

    # 2. Deadlock constraints: mọi transition đều không khả dụng
    for t in range(num_transitions):
        expr = []
        for p in range(num_places):
            is_input = (pn.I[t, p] == 1)
            is_output = (pn.O[t, p] == 1)
            if is_input:
                expr.append(1 - m_vars[p])  # input thiếu token
            if is_output and not is_input:
                expr.append(m_vars[p])      # output đã có token
        model += pulp.lpSum(expr) >= 1

    # Không cần tối ưu, chỉ cần nghiệm khả thi
    model.solve(pulp.PULP_CBC_CMD(msg=0))

    if pulp.LpStatus[model.status] != "Optimal":
        return []

    candidate = [int(pulp.value(m_vars[p])) for p in range(num_places)]
    return [candidate]

def validate_deadlocks_with_bdd(pn, bdd_mgr, reachable_bdd, candidates):
    places = pn.place_ids
    confirmed = []

    vars_map = {pid: f"{pid}_0" for pid in places}

    for m in candidates:
        expr_parts = []
        for val, pid in zip(m, places):
            varname = vars_map[pid]
            expr_parts.append(varname if val == 1 else f"!{varname}")
        expr_str = " & ".join(expr_parts)

        m_bdd = bdd_mgr.add_expr(expr_str)

        intersection = reachable_bdd & m_bdd
        if intersection.pick() is not None:   # dùng pick thay cho satisfy_one
            confirmed.append(m)

    return confirmed



def deadlock_reachable_marking(
    pn: PetriNet, 
    bdd_mgr: BDD, 
    reachable_bdd
) -> Optional[List[int]]:
    """
    Kết hợp ILP và BDD để phát hiện deadlock.
    """
    candidates = find_deadlock_candidates_ilp(pn)
    confirmed = validate_deadlocks_with_bdd(pn, bdd_mgr, reachable_bdd, candidates)
    if not confirmed:
        return None
    return confirmed[0]
