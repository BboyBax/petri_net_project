""" 
Task 1 - Thành viên 1
Đọc và phân tích file PNML để trích xuất các tập P, T, F.
"""

import xml.etree.ElementTree as ET

def parse_pnml(file_path: str):
    print("🔹 Đang đọc file PNML:", file_path)
    # TODO: Implement PNML parsing logic here
    # Basic skeleton: try to parse and extract places, transitions, arcs
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except Exception as e:
        print(f"Lỗi khi đọc PNML: {e}")
        return {
            "places": set(),
            "transitions": set(),
            "arcs": set()
        }

    # Note: PNML namespaces vary; real parsing should handle namespaces.
    places = set()
    transitions = set()
    arcs = set()

    for elem in root.iter():
        tag = elem.tag.split('}')[-1]
        if tag == 'place':
            pid = elem.attrib.get('id')
            if pid:
                places.add(pid)
        elif tag == 'transition':
            tid = elem.attrib.get('id')
            if tid:
                transitions.add(tid)
        elif tag == 'arc':
            aid = elem.attrib.get('id', None)
            source = elem.attrib.get('source')
            target = elem.attrib.get('target')
            arcs.add((source, target))

    return {
        "places": places,
        "transitions": transitions,
        "arcs": arcs
    }
