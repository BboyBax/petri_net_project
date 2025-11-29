""" 
Task 2 - Thành viên 2
Duyệt đồ thị trạng thái (explicit enumeration) từ net.
"""
from collections import deque
import numpy as np
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.task1_parser import PetriNet

from typing import Set, Tuple

def compute_reachability_bfs(pn: PetriNet) -> Set[Tuple[int, ...]]:
    visisted = set()
    queue = deque()

    M0_tuple = tuple(pn.M0)
    visisted.add(M0_tuple)
    queue.append(pn.M0)

    while queue:
        M_current = queue.popleft()

        for index in range(pn.I.shape[0]):
            I_current = pn.I[index]

            # Check token to fire
            if np.all(M_current >= I_current):
                O_current = pn.O[index]
                M_new = M_current - I_current + O_current

                # Require 1-safe
                if np.any(M_new > 1):
                    continue  

                M_new_tuple = tuple(M_new)

                if M_new_tuple not in visisted:
                    visisted.add(M_new_tuple)
                    queue.append(M_new)

    return visisted

def compute_reachability_dfs(pn: PetriNet) -> Set[Tuple[int, ...]]:
    visited = set()
    stack = deque()
    
    M0_tuple = tuple(pn.M0)
    visited.add(M0_tuple)
    stack.append(pn.M0)
    
    while stack:
        M_current = stack.pop()
        
        for index in range(pn.I.shape[0]):
            I_current = pn.I[index]
            
            if np.all(M_current >= I_current):
                O_current = pn.O[index]
                M_new = M_current - I_current + O_current
                
                
                if np.any(M_new > 1):
                    continue
                
                M_new_tuple = tuple(M_new)
                
                if M_new_tuple not in visited:
                    visited.add(M_new_tuple)
                    stack.append(M_new)   
                    
    return visited

def explicit_reachability(pn: PetriNet) -> Set[Tuple[int, ...]]:
    visisted_BFS = compute_reachability_bfs(pn)

    return visisted_BFS