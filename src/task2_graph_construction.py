""" 
Task 2 - Thành viên 2
Duyệt đồ thị trạng thái (explicit enumeration) từ net.
"""

from collections import deque

def build_state_graph(net):
    print("🔹 Đang xây dựng đồ thị trạng thái...")
    
    # Lấy marking đầu
    initial_marking = get_initial_marking(net)
    if initial_marking is None or not initial_marking:
        print("❌ Không tìm thấy initial marking!")
        return {
            'nodes': set(),
            'edges': set(),
            'initial_marking': None
        }
    
    # Chuyển dict sang tuple để hash được
    initial_marking_tuple = dict_to_tuple(initial_marking)
    
    # Khởi tạo BFS
    queue = deque([initial_marking_tuple])
    visited = {initial_marking_tuple}
    nodes = {initial_marking_tuple}
    edges = set()
    
    print(f"✓ Initial marking: {dict(initial_marking_tuple)}")
    state_count = 0
    
    # BFS
    while queue:
        current_marking_tuple = queue.popleft()
        current_marking = tuple_to_dict(current_marking_tuple)
        state_count += 1
        
        if state_count % 100 == 0:
            print(f"  Đã khám phá {state_count} trạng thái...")
        
        # Thử tất cả các transition
        for transition in get_transitions(net):
            trans_id = transition['id']
            
            if is_enabled(net, current_marking, trans_id):
                new_marking = fire_transition(net, current_marking, trans_id)
                new_marking_tuple = dict_to_tuple(new_marking)
                
                # Thêm node và edge
                nodes.add(new_marking_tuple)
                edges.add((current_marking_tuple, trans_id, new_marking_tuple))
                
                # Thêm vào queue nếu chưa visit
                if new_marking_tuple not in visited:
                    visited.add(new_marking_tuple)
                    queue.append(new_marking_tuple)
    
    print(f"✓ Hoàn thành! Tổng số trạng thái: {len(nodes)}")
    print(f"✓ Tổng số chuyển tiếp: {len(edges)}")
    
    return {
        'nodes': nodes,
        'edges': edges,
        'initial_marking': initial_marking_tuple
    }

# Lấy marking đầu từ dict net
def get_initial_marking(net):
    """Lấy initial marking từ dict net"""
    if not isinstance(net, dict):
        print("❌ net không phải dict!")
        return None
    
    if 'places' not in net:
        print("❌ Không có key 'places' trong net!")
        return None
    
    marking = {}
    for place in net['places']:
        if isinstance(place, dict):
            place_id = place.get('id')
            tokens = place.get('initialMarking', 0)
            marking[place_id] = tokens
        else:
            print(f"⚠️ Place không phải dict: {place}")
    
    if not marking:
        print("❌ Không có place nào được parse!")
        return None
    
    print(f"✓ Đã load {len(marking)} places")
    return marking

# Lấy tất cả transition từ dict net
def get_transitions(net):
    """Lấy danh sách transitions từ dict net"""
    if isinstance(net, dict) and 'transitions' in net:
        return net['transitions']
    return []

# Chuyển dict sang tuple để hash được
def dict_to_tuple(marking_dict):
    """Chuyển dict marking thành tuple có thể hash"""
    return tuple(sorted(marking_dict.items()))

# Chuyển tuple về dict
def tuple_to_dict(marking_tuple):
    """Chuyển tuple marking về dict"""
    return dict(marking_tuple)

# Kiểm tra transition có enabled không
def is_enabled(net, marking, transition_id):
    """Kiểm tra transition có enabled không dựa trên input arcs"""
    # Tìm tất cả input arcs của transition (place -> transition)
    for arc in net['arcs']:
        if arc['target'] == transition_id:  # arc từ place vào transition
            place_id = arc['source']
            weight = arc.get('weight', 1)
            
            # Kiểm tra place có đủ token không
            if marking.get(place_id, 0) < weight:
                return False
    
    return True

# Bắn transition và trả về marking mới
def fire_transition(net, marking, transition_id):
    """Bắn transition: trừ input tokens, cộng output tokens"""
    new_marking = marking.copy()
    
    # Trừ tokens từ input places (place -> transition)
    for arc in net['arcs']:
        if arc['target'] == transition_id:
            place_id = arc['source']
            weight = arc.get('weight', 1)
            new_marking[place_id] = new_marking.get(place_id, 0) - weight
    
    # Cộng tokens vào output places (transition -> place)
    for arc in net['arcs']:
        if arc['source'] == transition_id:
            place_id = arc['target']
            weight = arc.get('weight', 1)
            new_marking[place_id] = new_marking.get(place_id, 0) + weight
    
    return new_marking