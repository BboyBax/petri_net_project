""" 
Task 2 - Thành viên 2
Duyệt đồ thị trạng thái (explicit enumeration) từ net.
"""

from collections import deque

def build_state_graph(net):
    print("🔹 Đang xây dựng đồ thị trạng thái...")
    
    # lấy marking đầu
    initial_marking = get_initial_marking(net)
    if initial_marking is None:
        print("Không tìm thấy initial marking!")
        return {
            'nodes': set(),
            'edges': set(),
            'initial_marking': None
        }
    
    initial_marking_tuple = tuple(initial_marking)
    
    # Khởi tạo BFS
    queue = deque([initial_marking_tuple])
    visited = {initial_marking_tuple: True}
    nodes = {initial_marking_tuple}
    edges = set()
    
    print(f" Initial marking: {initial_marking_tuple}")
    state_count = 0
    
    #hàm BFS 
    while queue:
        current_marking = queue.popleft()
        state_count += 1
        
        if state_count % 10 == 0:
            print(f"Đã khám phá {state_count} trạng thái...")
        
        # Thử tất cả các transition
        for transition in get_transitions(net):
            if is_enabled(net, current_marking, transition):
                
                new_marking = fire_transition(net, current_marking, transition)
                new_marking_tuple = tuple(new_marking)
                
                
                nodes.add(new_marking_tuple)
                edges.add((current_marking, transition, new_marking_tuple))
                
                
                if new_marking_tuple not in visited:
                    visited[new_marking_tuple] = True
                    queue.append(new_marking_tuple)
    
    print(f"Hoàn thành! Tổng số trạng thái: {len(nodes)}")
    print(f"Tổng số chuyển tiếp: {len(edges)}")
    
    graph = {
        'nodes': nodes,
        'edges': edges,
        'initial_marking': initial_marking_tuple
    }
    return graph

#lấy marking đầu
def get_initial_marking(net):
    if hasattr(net, 'initial_marking'):
        return net.initial_marking
    elif hasattr(net, 'get_initial_marking'):
        return net.get_initial_marking()
    return None
#lấy tất cả transition
def get_transitions(net):
    if hasattr(net, 'transitions'):
        return net.transitions
    elif hasattr(net, 'get_transitions'):
        return net.get_transitions()
    return []
#kiểm tra transition có thê chạy không
def is_enabled(net, marking, transition):
    if hasattr(net, 'is_enabled'):
        return net.is_enabled(transition, list(marking))
    return True
#chạy transition
def fire_transition(net, marking, transition):
    if hasattr(net, 'fire_transition'):
        return net.fire_transition(transition, list(marking))
    return list(marking)