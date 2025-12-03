"""
Task 5: Tối ưu hóa trên các Marking có thể đạt được (dd.autoref)
"""

from typing import Tuple, List, Optional
import numpy as np
from dd.autoref import BDD, Function
import time
import tracemalloc
import psutil
import os


def max_reachable_marking(place_ids, R, c):
    bdd_mgr = R.bdd
    if R == bdd_mgr.false:
        return None, None
    if R == bdd_mgr.true:
        optimal_marking = [1 if ci > 0 else 0 for ci in c]
        return optimal_marking, int(np.dot(c, optimal_marking))

    optimal_marking, optimal_value = None, float('-inf')
    for assignment in bdd_mgr.pick_iter(R):
        marking = [1 if assignment.get(f"{pid}_0", False) else 0 for pid in place_ids]
        val = int(np.dot(c, marking))
        if val > optimal_value:
            optimal_value, optimal_marking = val, marking
    return optimal_marking, optimal_value

def evaluate_max_reachable_marking(place_ids, R, c):
    results = {}

    # Measuring the time and memory for the optimal marking search step
    tracemalloc.start()
    start = time.perf_counter()
    optimal_marking, optimal_value = max_reachable_marking(place_ids, R, c)
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    results['MaxReachableMarking'] = {
        'optimal_marking': optimal_marking,
        'optimal_value': optimal_value,
        'time': end - start,
        'memory_MB': peak / 1024**2
    }

    # Overall process memory
    process = psutil.Process(os.getpid())
    results['ProcessMemory_MB'] = process.memory_info().rss / 1024**2

    print("===== Max Reachable Marking Performance =====")
    for method, info in results.items():
        if isinstance(info, dict):
            print(f"{method}:")
            for k, v in info.items():
                print(f"  {k}: {v}")
        else:
            print(f"{method}: {info}")
    print("===========================================")

    return results

