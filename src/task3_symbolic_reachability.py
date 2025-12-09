""" 
Task 3 - Thành viên 3
Tính toán và biểu diễn reachable markings bằng BDD.
"""

import collections
from typing import Tuple, List, Optional, Dict, Iterator
from pyeda.inter import *
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.task1_parser import PetriNet
from src.task2_explicit_reachability import explicit_reachability
from collections import deque
import numpy as np

import time
import tracemalloc
import psutil

from dd.autoref import BDD



# Số bit mặc định (tăng nếu cần cho PNML có token > 2**BITS-1)
BITS = 1

# ----- helper -----
def bits_of(p: str) -> List[str]:
    return [f"{p}_{i}" for i in range(BITS)]

def bits_of_next(p: str) -> List[str]:
    return [f"{p}_next_{i}" for i in range(BITS)]

def bdd_iff(bdd: BDD, x, y):
    t1 = bdd.apply('and', x, y)
    t2 = bdd.apply('and', bdd.apply('not', x), bdd.apply('not', y))
    return bdd.apply('or', t1, t2)

def bdd_and(bdd: BDD, a, b):
    return bdd.apply('and', a, b)

def bdd_or(bdd: BDD, a, b):
    return bdd.apply('or', a, b)

def bdd_not(bdd: BDD, u):
    return bdd.apply('not', u)

# ----- build transition relation -----
def build_tr(bdd, places, transitions, arcs, pre_weight, post_weight):
    TR = bdd.false
    pre = {t: [] for t in transitions}
    post = {t: [] for t in transitions}

    for arc in arcs:
        s, t = arc['source'], arc['target']
        if s in places and t in transitions:
            pre[t].append(s)
        elif s in transitions and t in places:
            post[s].append(t)

    for t in transitions:
        enabled = bdd.true
        effect = bdd.true

        for p in places:
            x = bdd.var(bits_of(p)[0])
            nx = bdd.var(bits_of_next(p)[0])

            if p in pre[t] and p in post[t]:
                # self-loop: giữ nguyên
                effect = bdd_and(bdd, effect, bdd_iff(bdd, x, nx))
                enabled = bdd_and(bdd, enabled, x)  # cần token để bắn
            elif p in pre[t]:
                # input: cần token, rồi mất đi
                enabled = bdd_and(bdd, enabled, x)
                effect = bdd_and(bdd, effect, bdd_iff(bdd, nx, bdd.false))
            elif p in post[t]:
                # output: phải trống, rồi nhận token
                enabled = bdd_and(bdd, enabled, bdd_not(bdd, x))
                effect = bdd_and(bdd, effect, bdd_iff(bdd, nx, bdd.true))
            else:
                # không liên quan: giữ nguyên
                effect = bdd_and(bdd, effect, bdd_iff(bdd, x, nx))

        TR = bdd_or(bdd, TR, bdd_and(bdd, enabled, effect))

    return TR

# ----- reachable markings -----
def bdd_reachable(pn: PetriNet):
    """Trả về (bdd, R) với R là BDD đại diện cho tập reachable markings (dùng biến 'current')."""
    bdd = BDD()
    places = pn.place_ids
    transitions = pn.trans_ids
    arcs = pn.arcs_ids
    pre_weight = pn.pre_weight
    post_weight = pn.post_weight

    # khai báo biến current và next
    for p in places:
        for b in bits_of(p):
            bdd.add_var(b)
        for b in bits_of_next(p):
            bdd.add_var(b)

    # Khởi tạo R từ M0 (đúng theo pn.M0)
    R = bdd.true
    for idx, p in enumerate(places):
        val = pn.M0[idx]
        for i, bitname in enumerate(bits_of(p)):
            bit = bdd.var(bitname)
            if ((val >> i) & 1) == 1:
                R = bdd_and(bdd, R, bit)
            else:
                R = bdd_and(bdd, R, bdd_not(bdd, bit))

    TR = build_tr(bdd, places, transitions, arcs, pre_weight, post_weight)

    # Post operator: ∃current . (R ∧ TR), rồi đổi next -> current
    def Post(Rb):
        elim = []
        for p in places:
            elim.extend(bits_of(p))
        step = bdd.exist(elim, bdd_and(bdd, Rb, TR))
        rename = {f"{p}_next_{i}": f"{p}_{i}" for p in places for i in range(BITS)}
        return bdd.let(rename, step)

    old = bdd.false
    iteration = 0
    while R != old:
        old = R
        R = bdd_or(bdd, R, Post(R))
        iteration += 1
        if iteration > 10000:
            break

    return bdd, R

# Helper: enumerate reachable markings (may be large)
def extract_markings(bdd: BDD, R, places: List[str]) -> Iterator[Dict[str, int]]:
    for assignment in bdd.pick_iter(R):
        marking = {}
        for p in places:
            val = 0
            for i in range(BITS):
                vname = f"{p}_{i}"
                bit = assignment.get(vname, False)
                if bit:
                    val |= (1 << i)
            marking[p] = val
        yield marking

def compare_methods(pn: PetriNet):
    results = {}
    tracemalloc.start()
    start = time.perf_counter()
    bdd, R = bdd_reachable(pn)
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    results['BDD'] = {
        'count': sum(1 for _ in extract_markings(bdd, R, pn.place_ids)), 
        'time': end - start,
        'memory_MB': peak / 1024**2
    }

    tracemalloc.start()
    start = time.perf_counter()
    explicit_states = explicit_reachability(pn)
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    results['Explicit'] = {
        'count': len(explicit_states),
        'time': end - start,
        'memory_MB': peak / 1024**2
    }

    process = psutil.Process(os.getpid())
    results['ProcessMemory_MB'] = process.memory_info().rss / 1024**2

    print("===== Compare BDD with Explicit =====")
    for method, info in results.items():
        print(f"{method}:")
        if isinstance(info, dict):
            for k, v in info.items():
                print(f"  {k}: {v}")
        else:
            print(f"  {info}")
    print("===================================")
    return results
