""" 
Task 1 - Thành viên 1
Đọc và phân tích file PNML để trích xuất các tập P, T, F.
"""

import xml.etree.ElementTree as ET

def parse_pnml(file_path):
    """Parse file PNML và trả về cấu trúc Petri Net đầy đủ cho Task 2 & Task 3"""
    
    tree = ET.parse(file_path)
    root = tree.getroot()

    ns = {'pnml': 'http://www.pnml.org/version-2009/grammar/pnml'}

    places = []
    transitions = []
    arcs = []
    initial_marking = {}

    print(f"Parsing {file_path}...")

    # ============================================================
    # 1) Parse places + marking
    # ============================================================
    for place in root.findall('.//pnml:place', ns):
        pid = place.get('id')

        # Initial marking
        marking_elem = place.find('pnml:initialMarking/pnml:text', ns)
        marking_val = int(marking_elem.text) if marking_elem is not None else 0

        places.append(pid)
        initial_marking[pid] = marking_val

        print(f"  Place: {pid} = {marking_val} tokens")

    # ============================================================
    # 2) Parse transitions
    # ============================================================
    for transition in root.findall('.//pnml:transition', ns):
        tid = transition.get('id')
        transitions.append(tid)

        print(f"  Transition: {tid}")

    # ============================================================
    # 3) Parse arcs (source, target, weight)
    # ============================================================
    for arc in root.findall('.//pnml:arc', ns):
        aid = arc.get('id')
        s = arc.get('source')
        t = arc.get('target')

        # Default weight = 1
        w_elem = arc.find('.//pnml:text', ns)
        w = int(w_elem.text) if w_elem is not None else 1

        arcs.append({
            "id": aid,
            "source": s,
            "target": t,
            "weight": w
        })

        print(f"  Arc: {s} -> {t} (w={w})")

    print(f"Parsed: {len(places)} places, {len(transitions)} transitions, {len(arcs)} arcs")

    # ============================================================
    # 4) Build pre_weight & post_weight dictionaries
    # ============================================================
    pre_weight = {}
    post_weight = {}

    for arc in arcs:
        s = arc["source"]
        t = arc["target"]
        w = arc["weight"]

        if s in places and t in transitions:
            # Place → Transition
            pre_weight[(s, t)] = w

        elif s in transitions and t in places:
            # Transition → Place
            post_weight[(s, t)] = w

    # ============================================================
    # Return full Petri Net spec
    # ============================================================
    return {
        "places": places,
        "transitions": transitions,
        "arcs": arcs,
        "pre_weight": pre_weight,
        "post_weight": post_weight,
        "initial_marking": initial_marking
    }
