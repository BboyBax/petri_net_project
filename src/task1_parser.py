""" 
Task 1 - Thành viên 1
Đọc và phân tích file PNML để trích xuất các tập P, T, F.
"""

import numpy as np
import xml.etree.ElementTree as ET
from typing import List, Optional

class PetriNet:
    def __init__(
        self,
        place_ids: List[str],
        trans_ids: List[str],
        place_names: List[Optional[str]],
        trans_names: List[Optional[str]],
        I: np.ndarray,   
        O: np.ndarray, 
        M0: np.ndarray
    ):
        self.place_ids = place_ids
        self.trans_ids = trans_ids
        self.place_names = place_names
        self.trans_names = trans_names
        self.I = I
        self.O = O
        self.M0 = M0

    @classmethod
    def from_pnml(cls, filename: str) -> "PetriNet":
        ## TODO read file PNML
        tree = ET.parse(filename)
        root = tree.getroot()

        ns = {'pnml': 'http://www.pnml.org/version-2009/grammar/pnml'}

        # ============================================================
        # 1) Parse places + marking
        # ============================================================

        place_id = []
        place_names = []
        place_id_to_index = {}
        initial_marking = []

        for index, place in enumerate(root.findall('.//pnml:place', ns)):
            # Place ID
            pid = place.get('id')
            place_id.append(pid)
            place_id_to_index[pid] = index

            # Place Name
            name_place = place.find('.//pnml:name/pnml:text', ns)
            p_name = name_place.text if name_place is not None else None
            place_names.append(p_name)

            # Initial marking
            marking_elem = place.find('pnml:initialMarking/pnml:text', ns)
            marking_val = int(marking_elem.text) if marking_elem is not None else 0
            initial_marking.append(marking_val)

        # ============================================================
        # 2) Parse transitions
        # ============================================================
        
        trans_id = []
        trans_names = []
        trans_id_to_index = {}

        for index, transition in enumerate(root.findall('.//pnml:transition', ns)):
            # Transition ID
            tid = transition.get('id')
            trans_id.append(tid)
            trans_id_to_index[tid] = index

            # Transition Name
            name_transition = transition.find('.//pnml:name/pnml:text', ns)
            t_name = name_transition.text if name_transition is not None else None
            trans_names.append(t_name)

            # Inital matrix I, O, M0
            num_places = len(place_id)
            num_trans = len(trans_id)

            I = np.zeros((num_trans, num_places), dtype=int)
            O = np.zeros((num_trans, num_places), dtype=int)
            M0 = np.array(initial_marking, dtype=int)

        # ============================================================
        # 3) Parse arcs (source, target, weight)
        # ============================================================    

        for arc in root.findall('.//pnml:arc', ns):
            # Inital Arc
            aid = arc.get('id')
            source = arc.get('source')
            target = arc.get('target')

            # Default weight = 1
            weight_elem = arc.find('.//pnml:text', ns)
            weight = int(weight_elem.text) if weight_elem is not None else 1

            # Inital value of matrix I, O
            if source in place_id_to_index and target in trans_id_to_index:
                # Place -> Transition (Input matrix)
                pid = place_id_to_index[source]
                tid = trans_id_to_index[target]
                I[tid, pid] = weight
            elif source in trans_id_to_index and target in place_id_to_index:
                # Transition -> Place (Output matrix)
                tid = trans_id_to_index[source]
                pid = place_id_to_index[target]
                O[tid, pid] = weight

        return cls(place_id, trans_id, place_names, trans_names, I, O, M0)

    def __str__(self) -> str:
        s = []
        s.append("Places: " + str(self.place_ids))
        s.append("Place names: " + str(self.place_names))
        s.append("\nTransitions: " + str(self.trans_ids))
        s.append("Transition names: " + str(self.trans_names))
        s.append("\nI (input) matrix:")
        s.append(str(self.I))
        s.append("\nO (output) matrix:")
        s.append(str(self.O))
        s.append("\nInitial marking M0:")
        s.append(str(self.M0))
        return "\n".join(s)
