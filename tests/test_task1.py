import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.task1_parser import PetriNet

from pathlib import Path

# def test_001():
#     base_dir = Path(__file__).parent.parent / "data" / "pnml"
#     pn = PetriNet.from_pnml(str(base_dir / "example.pnml"))

#     with open(base_dir / "expected.txt", "r", encoding="utf-8") as f:
#         expected_content = f.read().strip()
        
#     actual_content = str(pn).strip()
#     assert actual_content == expected_content, "PetriNet.from_pnml output does not match expected"

def test_002():
    base_dir = Path(__file__).parent.parent / "data" / "pnml"
    pn = PetriNet.from_pnml(str(base_dir / "phylosopher.pnml"))
    print(pn)   