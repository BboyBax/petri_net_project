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
        arcs_ids: List[dict],
        place_names: List[Optional[str]],
        trans_names: List[Optional[str]],
        I: np.ndarray,   
        O: np.ndarray, 
        M0: np.ndarray,
        pre_weight: dict,
        post_weight: dict
    ):
        self.place_ids = place_ids
        self.trans_ids = trans_ids
        self.arcs_ids = arcs_ids
        self.place_names = place_names
        self.trans_names = trans_names
        self.I = I
        self.O = O
        self.M0 = M0
        self.pre_weight = pre_weight
        self.post_weight = post_weight

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

        places = root.findall('.//pnml:place', ns)
        for index, place in enumerate(places):
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
        transitions = root.findall('.//pnml:transition', ns)
        for index, transition in enumerate(transitions):
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

        

        arcs = root.findall('.//pnml:arc', ns)
        arc_ids = [] 
        for arc in arcs:
            # Inital Arc
            aid = arc.get('id')
            source = arc.get('source')
            target = arc.get('target')
            
            # Default weight = 1
            weight_elem = arc.find('.//pnml:text', ns)
            weight = int(weight_elem.text) if weight_elem is not None else 1
            arc_ids.append({'source': source, 'target': target, 'weight': weight})
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
        # ============================================================
        # 4) Build pre_weight & post_weight dictionaries
        # ============================================================

        pre_weight = {}
        post_weight = {}
        for arc in arcs:
            s = arc.get("source")
            t = arc.get("target")

            # Get the weight from the text content inside the arc
            weight_elem = arc.find(".//pnml:text", ns)
            w = int(weight_elem.text) if weight_elem is not None else 1

            if s in places and t in transitions:
                # Place → Transition
                pre_weight[(s, t)] = w

            elif s in transitions and t in places:
                # Transition → Place
                post_weight[(s, t)] = w    

        return cls(place_id, trans_id, arc_ids, place_names, trans_names, I, O, M0, pre_weight, post_weight)

    def validate(self) -> list[str]:
        """
        Check for critical errors in the Petri Net. 
        Return a list of errors (empty if there are none).
        """
        errors = []

        # 1. Check ID is empty
        for pid in self.place_ids:
            if not pid or pid.strip() == "":
                errors.append("Place ID is missing or empty")
        for tid in self.trans_ids:
            if not tid or tid.strip() == "":
                errors.append("Transition ID is missing or empty")

        # 2. Check for duplicate IDs within the same category
        if len(self.place_ids) != len(set(self.place_ids)):
            errors.append("Duplicate Place IDs detected")
        if len(self.trans_ids) != len(set(self.trans_ids)):
            errors.append("Duplicate Transition IDs detected")

        # 3. Check for duplicate IDs between Place and Transition (optional)
        overlap = set(self.place_ids).intersection(set(self.trans_ids))
        if overlap:
            errors.append(f"ID used as both Place and Transition: {overlap}")

        # 4. Check for negative marking 
        for i, m in enumerate(self.M0):
            if m < 0:
                errors.append(f"Initial marking of place {self.place_ids[i]} is negative: {m}")

        # 5. Check arcs
        valid_ids = set(self.place_ids) | set(self.trans_ids)
        for arc in self.arcs_ids:
            s, t, w = arc['source'], arc['target'], arc['weight']

            if s not in valid_ids:
                errors.append(f"Arc source not found: {s}")
            if t not in valid_ids:
                errors.append(f"Arc target not found: {t}")

            if (s in self.place_ids and t in self.place_ids) or \
               (s in self.trans_ids and t in self.trans_ids):
                errors.append(f"Invalid arc structure: {s} -> {t}")

            if not isinstance(w, int) or w <= 0:
                errors.append(f"Invalid arc weight {w} for arc {s}->{t}")

        return errors

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
        s.append("\nPre_weight matrix:")
        s.append(str(self.pre_weight))  
        s.append("\nPost_weight matrix:")
        s.append(str(self.post_weight))  
        s.append("\nArcs:")
        s.append(str(self.arcs_ids))     
        return "\n".join(s)

    
  
