import xml.etree.ElementTree as ET

def parse_pnml(file_path):
    """Parse file PNML và trả về cấu trúc Petri net"""
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Namespace
    ns = {'pnml': 'http://www.pnml.org/version-2009/grammar/pnml'}
    
    places = []
    transitions = []
    arcs = []
    
    print(f"🔍 Parsing {file_path}...")
    
    # Parse places
    for place in root.findall('.//pnml:place', ns):
        place_id = place.get('id')
        
        # Lấy initial marking
        marking_elem = place.find('pnml:initialMarking/pnml:text', ns)
        initial_marking = int(marking_elem.text) if marking_elem is not None else 0
        
        place_dict = {
            'id': place_id,
            'initialMarking': initial_marking
        }
        places.append(place_dict)
        print(f"  Place: {place_id} = {initial_marking} tokens")
    
    # Parse transitions
    for transition in root.findall('.//pnml:transition', ns):
        trans_id = transition.get('id')
        transitions.append({
            'id': trans_id
        })
        print(f"  Transition: {trans_id}")
    
    # Parse arcs
    for arc in root.findall('.//pnml:arc', ns):
        arc_id = arc.get('id')
        source = arc.get('source')
        target = arc.get('target')
        
        arcs.append({
            'id': arc_id,
            'source': source,
            'target': target,
            'weight': 1
        })
        print(f"  Arc: {source} -> {target}")
    
    print(f"✓ Parsed: {len(places)} places, {len(transitions)} transitions, {len(arcs)} arcs")
    
    return {
        'places': places,
        'transitions': transitions,
        'arcs': arcs
    }