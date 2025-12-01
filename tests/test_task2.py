import numpy as np
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.task1_parser import PetriNet
from src.task2_graph_construction import explicit_reachability
from pathlib import Path
import pytest

def test_001():
    base_dir = Path(__file__).parent.parent / "data" / "pnml"
    pn = PetriNet.from_pnml(str(base_dir / "example.pnml"))
    errors = pn.validate()
    if errors:
        print("Validation errors found:")
        for e in errors:
            print(" -", e)
    else:
        output = explicit_reachability(pn)
        expected = {
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1)
        }
        assert output == expected


def test_002():
    base_dir = Path(__file__).parent.parent / "data" / "pnml"
    pn = PetriNet.from_pnml(str(base_dir / "phylosopher.pnml"))
    errors = pn.validate()
    if errors:
        print("Validation errors found:")
        for e in errors:
            print(" -", e)
    else:
        output = explicit_reachability(pn)
        output = len(output)
        expected = 82
        assert output == expected

def test_003():
    base_dir = Path(__file__).parent.parent / "data" / "pnml"
    pn = PetriNet.from_pnml(str(base_dir / "example2.pnml"))
    errors = pn.validate()
    if errors:
        print("Validation errors found:")
        for e in errors:
            print(" -", e)
    else:
        output = explicit_reachability(pn)
        output = len(output)
        expected = 4
        assert output == expected

# def test_004():
#     base_dir = Path(__file__).parent.parent / "data" / "pnml"
#     pn = PetriNet.from_pnml(str(base_dir / "example3.pnml"))
#     print(pn)   # In ra để kiểm tra
#     output = explicit_reachability(pn)  
#     print("Reachable markings:", len(output))    