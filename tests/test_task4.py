import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.task4_ilp_formulation import deadlock_reachable_marking
from src.task1_parser import PetriNet
from src.task3_bdd_computation import bdd_reachable, compare_methods, print_all_markings_bdd
from src.task2_graph_construction import explicit_reachability, print_all_markings
from pyeda.inter import *
import pytest
import numpy as np
from pathlib import Path


def test_001():
    base_dir = Path(__file__).parent.parent / "data" / "pnml"
    pn = PetriNet.from_pnml(str(base_dir / "deadlock1.pnml"))
    errors = pn.validate()
    if errors:
        print("Validation errors found:")
        for e in errors:
            print(" -", e)
    else:
        bdd, R = bdd_reachable(pn)
        marking = deadlock_reachable_marking(pn, bdd, R)
        print(marking)

def test_002():
    base_dir = Path(__file__).parent.parent / "data" / "pnml"
    pn = PetriNet.from_pnml(str(base_dir / "deadlock2.pnml"))
    errors = pn.validate()
    if errors:
        print("Validation errors found:")
        for e in errors:
            print(" -", e)
    else:
        bdd, R = bdd_reachable(pn)
        marking = deadlock_reachable_marking(pn, bdd, R)
        print(marking)

def test_003():
    base_dir = Path(__file__).parent.parent / "data" / "pnml"
    pn = PetriNet.from_pnml(str(base_dir / "deadlock3.pnml"))
    errors = pn.validate()
    if errors:
        print("Validation errors found:")
        for e in errors:
            print(" -", e)
    else:
        bdd, R = bdd_reachable(pn)
        marking = deadlock_reachable_marking(pn, bdd, R)
        print(marking)
def test_004():
    base_dir = Path(__file__).parent.parent / "data" / "pnml"
    pn = PetriNet.from_pnml(str(base_dir / "deadlock4.pnml"))
    errors = pn.validate()
    if errors:
        print("Validation errors found:")
        for e in errors:
            print(" -", e)
    else:
        bdd, R = bdd_reachable(pn)
        marking = deadlock_reachable_marking(pn, bdd, R)
        print(marking)   