import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.task1_parser import PetriNet

from pathlib import Path

def test_001():
    base_dir = Path(__file__).parent.parent / "data" / "pnml"
    pn = PetriNet.from_pnml(str(base_dir / "example.pnml"))
    errors = pn.validate()
    if errors:
        print("Validation errors found:")
        for e in errors:
            print(" -", e)
    else:
        print("Validation passed: Petri Net structure is consistent.")
        print(pn)   # chỉ in cấu trúc khi không có lỗi


def test_002():
    base_dir = Path(__file__).parent.parent / "data" / "pnml"
    pn = PetriNet.from_pnml(str(base_dir / "phylosopher.pnml"))
    errors = pn.validate()
    if errors:
        print("Validation errors found:")
        for e in errors:
            print(" -", e)
    else:
        print("Validation passed: Petri Net structure is consistent.")
        print(pn)   # chỉ in cấu trúc khi không có lỗi