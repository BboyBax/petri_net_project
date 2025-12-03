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

import time
import tracemalloc
import psutil


def find_deadlock_candidates_ilp(pn: PetriNet) -> List[List[int]]:
    num_places = len(pn.place_ids)
    num_transitions = pn.I.shape[0]

    # ILP variable: m_p for each place
    m_vars = [pulp.LpVariable(f"m_{i}", lowBound=0, upBound=1, cat="Integer") 
              for i in range(num_places)]
    sigma_vars = [pulp.LpVariable(f"sigma_{t}", lowBound=0, upBound=1, cat="Integer") 
                  for t in range(num_transitions)]

    # Mô hình ILP
    model = pulp.LpProblem("DeadlockDetection", pulp.LpMinimize)

    # 1. State equation: m = M0 + C * sigma
    C = pn.O - pn.I
    for p in range(num_places):
        model += m_vars[p] == pn.M0[p] + pulp.lpSum(C[t, p] * sigma_vars[t] for t in range(num_transitions))

    # 2. Deadlock constraints: all transitions are unavailable
    for t in range(num_transitions):
        expr = []
        for p in range(num_places):
            is_input = (pn.I[t, p] == 1)
            is_output = (pn.O[t, p] == 1)
            if is_input:
                expr.append(1 - m_vars[p])  # input lacks token
            if is_output and not is_input:
                expr.append(m_vars[p])      # output has token
        model += pulp.lpSum(expr) >= 1

    # No need to optimize, just need a feasible solution
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
        if intersection.pick() is not None:   # use pick instead of satisfy_one
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

def evaluate_deadlock_detection(pn, bdd_mgr, reachable_bdd):
    results = {}

    # Measuring time and memory for the ILP + BDD step
    tracemalloc.start()
    start = time.perf_counter()
    deadlock = deadlock_reachable_marking(pn, bdd_mgr, reachable_bdd)
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    results['DeadlockDetection'] = {
        'deadlock': deadlock,
        'time': end - start,
        'memory_MB': peak / 1024**2
    }

    # Overall process memory
    process = psutil.Process(os.getpid())
    results['ProcessMemory_MB'] = process.memory_info().rss / 1024**2

    print("===== Deadlock Detection Performance =====")
    for method, info in results.items():
        print(f"{method}:")
        if isinstance(info, dict):
            for k, v in info.items():
                print(f"  {k}: {v}")
        else:
            print(f"  {info}")
    print("========================================")

    return results
