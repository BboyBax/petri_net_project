# """ 
# Task 3 - Thành viên 3
# Tính toán và biểu diễn reachable markings bằng BDD.
# """

# # places = ["p1", "p2", "p3", ...]
# # transitions = ["t1", "t2", "t3", ...]
# # arcs = [
# #     {"source": "p1", "target": "t1"},
# #     {"source": "t1", "target": "p2"},
# #     ...
# # ]

# from dd.autoref import BDD

# import math

# BITS = 3 # Ex: MAX_TOKEN = 7 -> 3 bits

# def bits_of(p):
#     return [f"{p}_{i}" for i in range(BITS)]

# def bits_of_next(p):
#     return [f"{p}_next_{i}" for i in range(BITS)]

# def const_bits(c):
#     # return list 3 bit -> boole (0/1)
#     return [(c >> i) & 1 for i in range(BITS)]

# def bdd_ge(bdd, x_bits, y_bits):
#     """
#     x_bits: danh sách biến bit của place p
#     y_bits: CONSTANT bits (0/1)
#     """
#     # GE logic: x >= y là OR trên tất cả prefix (x > y) hoặc full equal
#     ge = bdd.false
#     equal_prefix = bdd.true

#     # duyệt từ MSB → LSB
#     for i in reversed(range(BITS)):
#         x = bdd.var(x_bits[i])
#         y = bdd.true if y_bits[i] == 1 else bdd.false

#         # x > y tại bit i
#         greater = x & ~y

#         ge |= equal_prefix & greater

#         # update equal_prefix
#         equal_prefix &= ((x & y) | (~x & ~y))

#     # x == y case
#     ge |= equal_prefix
#     return ge

# def bdd_add_const(bdd, x_bits, delta, next_bits):
#     """x_next = x + delta (delta có thể âm). Hỗ trợ autoref bằng apply()."""

#     const = const_bits(delta & ((1 << BITS) - 1))

#     carry = bdd.false
#     first = True
#     constraints = bdd.true

#     for i in range(BITS):
#         x = bdd.var(x_bits[i])
#         c = bdd.true if const[i] else bdd.false
#         nx = bdd.var(next_bits[i])

#         if first:
#             # s = x XOR c
#             s = bdd.apply('xor', x, c)
#             # carry = x AND c
#             carry = bdd.apply('and', x, c)
#             first = False
#         else:
#             # s = x XOR c XOR carry
#             t = bdd.apply('xor', x, c)
#             s = bdd.apply('xor', t, carry)

#             # carry_next = (x AND c) OR (x AND carry) OR (c AND carry)
#             term1 = bdd.apply('and', x, c)
#             term2 = bdd.apply('and', x, carry)
#             term3 = bdd.apply('and', c, carry)

#             tmp = bdd.apply('or', term1, term2)
#             carry = bdd.apply('or', tmp, term3)

#         # constraint: nx == s
#         eq = (nx & s) | (~nx & ~s)
#         constraints = bdd.apply('and', constraints, eq)

#     return constraints


# def build_tr(bdd, places, transitions, arcs, pre_weight, post_weight):
#     TR = bdd.false

#     # build pre and post lists
#     pre = {t: [] for t in transitions}
#     post = {t: [] for t in transitions}

#     for arc in arcs:
#         s, t = arc["source"], arc["target"]
#         if s in places and t in transitions:
#             pre[t].append(s)
#         elif s in transitions and t in places:
#             post[s].append(t)

#     for t in transitions:
#         # 1) enabled(t): tất cả M(p) >= preWeight(p,t)
#         enabled = bdd.true
#         for p in pre[t]:
#             x_bits = bits_of(p)
#             w = pre_weight[(p, t)]
#             enabled &= bdd_ge(bdd, x_bits, const_bits(w))

#         # 2) effect: p_next = p - pre + post
#         effect = bdd.true
#         for p in places:
#             x_bits = bits_of(p)
#             nx_bits = bits_of_next(p)

#             delta = 0
#             if p in pre[t]:
#                 delta -= pre_weight[(p, t)]
#             if p in post[t]:
#                 delta += post_weight[(t, p)]

#             effect &= bdd_add_const(bdd, x_bits, delta, nx_bits)

#         # TR_t = enabled ∧ effect
#         TR |= enabled & effect

#     return TR

# def symbolic_reachability(places, transitions, arcs, pre_weight, post_weight, initial_marking):
#     bdd = BDD()
#     bdd.configure(reordering=True)

#     # create BDD vars for all bits
#     for p in places:
#         for b in bits_of(p):
#             bdd.add_var(b)
#         for b in bits_of_next(p):
#             bdd.add_var(b)

#     # Initial marking R
#     R = bdd.true
#     for p in places:
#         val = initial_marking[p]
#         for i, bitname in enumerate(bits_of(p)):
#             bit = bdd.var(bitname)
#             if (val >> i) & 1:
#                 R &= bit
#             else:
#                 R &= ~bit

#     # Build TR BDD
#     TR = build_tr(bdd, places, transitions, arcs, pre_weight, post_weight)

#     # Post operator
#     # def Post(R):
#     #     # exist elimination on current bits
#     #     elim = sum((bits_of(p) for p in places), [])
#     #     step = bdd.exist(elim, R & TR)

#     #     # rename next_bits → bits
#     #     rename = {}
#     #     for p in places:
#     #         for i in range(BITS):
#     #             rename[f"{p}_next_{i}"] = f"{p}_{i}"

#     #     return step.let(rename)

#     def Post(R):
#         # 1) Existential quantification trên các biến hiện tại
#         elim = sum((bits_of(p) for p in places), [])
#         step = bdd.exist(elim, R & TR)

#         # 2) rename next_bits → current bits
#         rename = {}
#         for p in places:
#             for i in range(BITS):
#                 rename[f"{p}_next_{i}"] = f"{p}_{i}"

#         # 3) autoref dùng dạng: bdd.let(mapping, function)
#         return bdd.let(rename, step)



#     # fixed point
#     old = bdd.false
#     while R != old:
#         old = R
#         R |= Post(R)

#     return bdd, R

#     # return {
#     #     'bdd_repr': None,
#     #     'vars': []
#     # }

"""
Module: task3_bdd_computation.py
Phiên bản tương thích dd.autoref (Windows-friendly).

Hàm chính:
- symbolic_reachability(places, transitions, arcs, pre_weight, post_weight, initial_marking)
  Trả về (bdd, R) với R là BDD của tập reachable markings (sử dụng biến hiện tại).

- compute_bdd(petri_net)  - wrapper nhận petri_net dict từ parse_pnml

- extract_markings(bdd, R, places) - helper trả về iterator các marking (dict place->int)

Ghi chú:
- Biến tên theo mẫu: p_{i} cho bit i (LSB i=0), p_next_{i} cho trạng thái tiếp theo.
- BITS có thể sửa (mặc định 3 => max token 7). Nếu PNML có token lớn hơn, tăng BITS.
- Sử dụng API dd.autoref (bdd.apply, bdd.let, bdd.exist, bdd.pick_iter) để tương thích Windows.
"""

from dd.autoref import BDD
import math
from typing import Dict, List, Tuple, Iterator

# Số bit mặc định (tăng nếu cần cho PNML có token > 2**BITS-1)
BITS = 3

# ----- helper tên biến -----
def bits_of(p: str) -> List[str]:
    return [f"{p}_{i}" for i in range(BITS)]


def bits_of_next(p: str) -> List[str]:
    return [f"{p}_next_{i}" for i in range(BITS)]


def const_bits(c: int) -> List[int]:
    return [(c >> i) & 1 for i in range(BITS)]


# ----- BDD helpers sử dụng bdd.apply -----
def bdd_not(bdd: BDD, u):
    return bdd.apply('not', u)


def bdd_and(bdd: BDD, a, b):
    return bdd.apply('and', a, b)


def bdd_or(bdd: BDD, a, b):
    return bdd.apply('or', a, b)


def bdd_xor(bdd: BDD, a, b):
    return bdd.apply('xor', a, b)


# x_bits are names (strings) of variables
# y_bits is list of constant bits (0/1)
def bdd_ge(bdd: BDD, x_bits: List[str], y_bits: List[int]):
    # x >= y
    ge = bdd.false
    equal_prefix = bdd.true

    # iterate MSB -> LSB
    for i in reversed(range(BITS)):
        x = bdd.var(x_bits[i])
        y = bdd.true if y_bits[i] == 1 else bdd.false

        # greater = x & ~y
        greater = bdd_and(bdd, x, bdd_not(bdd, y))

        ge = bdd_or(bdd, ge, bdd_and(bdd, equal_prefix, greater))

        # equal_prefix &= (x == y)  -> (x & y) | (~x & ~y)
        term1 = bdd_and(bdd, x, y)
        term2 = bdd_and(bdd, bdd_not(bdd, x), bdd_not(bdd, y))
        equal_prefix = bdd_and(bdd, equal_prefix, bdd_or(bdd, term1, term2))

    # x == y case
    ge = bdd_or(bdd, ge, equal_prefix)
    return ge


# Thực hiện x + delta → p_next. Delta có thể âm
# Triển khai cộng nhị phân với carry.
def bdd_add_const(bdd: BDD, x_bits: List[str], delta: int, next_bits: List[str]):
    const = const_bits(delta & ((1 << BITS) - 1))

    carry = bdd.false
    first = True
    constraints = bdd.true

    for i in range(BITS):
        x = bdd.var(x_bits[i])
        c = bdd.true if const[i] else bdd.false
        nx = bdd.var(next_bits[i])

        if first:
            s = bdd_xor(bdd, x, c)
            carry = bdd_and(bdd, x, c)
            first = False
        else:
            t = bdd_xor(bdd, x, c)
            s = bdd_xor(bdd, t, carry)

            term1 = bdd_and(bdd, x, c)
            term2 = bdd_and(bdd, x, carry)
            term3 = bdd_and(bdd, c, carry)

            tmp = bdd_or(bdd, term1, term2)
            carry = bdd_or(bdd, tmp, term3)

        # constraint nx == s  -> (nx & s) | (~nx & ~s)
        eq1 = bdd_and(bdd, nx, s)
        eq2 = bdd_and(bdd, bdd_not(bdd, nx), bdd_not(bdd, s))
        eq = bdd_or(bdd, eq1, eq2)

        constraints = bdd_and(bdd, constraints, eq)

    return constraints


def build_tr(bdd: BDD,
             places: List[str],
             transitions: List[str],
             arcs: List[Dict],
             pre_weight: Dict[Tuple[str, str], int],
             post_weight: Dict[Tuple[str, str], int]):
    TR = bdd.false

    # build pre and post lists
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
        for p in pre[t]:
            x_bits = bits_of(p)
            w = pre_weight.get((p, t), 1)
            enabled = bdd_and(bdd, enabled, bdd_ge(bdd, x_bits, const_bits(w)))

        effect = bdd.true
        for p in places:
            x_bits = bits_of(p)
            nx_bits = bits_of_next(p)

            delta = 0
            if p in pre[t]:
                delta -= pre_weight.get((p, t), 1)
            if p in post[t]:
                delta += post_weight.get((t, p), 1)

            effect = bdd_and(bdd, effect, bdd_add_const(bdd, x_bits, delta, nx_bits))

        TR = bdd_or(bdd, TR, bdd_and(bdd, enabled, effect))

    return TR


def symbolic_reachability(places: List[str],
                          transitions: List[str],
                          arcs: List[Dict],
                          pre_weight: Dict[Tuple[str, str], int],
                          post_weight: Dict[Tuple[str, str], int],
                          initial_marking: Dict[str, int]):
    """Trả về (bdd, R) với R là BDD đại diện cho tập reachable markings (dùng biến "current")."""

    bdd = BDD()
    # reordering có thể bật/tắt; autoref hỗ trợ cấu hình tối giản
    # bdd.configure(reordering=True)

    # tạo biến
    for p in places:
        for b in bits_of(p):
            bdd.add_var(b)
        for b in bits_of_next(p):
            bdd.add_var(b)

    # Initial R
    R = bdd.true
    for p in places:
        val = initial_marking.get(p, 0)
        for i, bitname in enumerate(bits_of(p)):
            bit = bdd.var(bitname)
            if ((val >> i) & 1) == 1:
                R = bdd_and(bdd, R, bit)
            else:
                R = bdd_and(bdd, R, bdd_not(bdd, bit))

    TR = build_tr(bdd, places, transitions, arcs, pre_weight, post_weight)

    # Post operator
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
        # optional: break safety if too many iterations
        if iteration > 10000:
            break

    return bdd, R


# Wrapper convenient
def compute_bdd(petri_net: Dict):
    return symbolic_reachability(
        petri_net['places'],
        petri_net['transitions'],
        petri_net['arcs'],
        petri_net['pre_weight'],
        petri_net['post_weight'],
        petri_net['initial_marking']
    )


# Helper: enumerate reachable markings (may be large)
def extract_markings(bdd: BDD, R, places: List[str]) -> Iterator[Dict[str, int]]:
    # pick_iter trả về assignments cho tất cả biến
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
