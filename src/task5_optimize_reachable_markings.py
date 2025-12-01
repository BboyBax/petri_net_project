"""
Task 5: Tối ưu hóa trên các Marking có thể đạt được (dd.autoref)
"""

from typing import Tuple, List, Optional
import numpy as np
from dd.autoref import BDD, Function


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

