import numpy as np
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.task1_parser import PetriNet
from src.task2_graph_construction import explicit_reachability, print_all_markings
from src.task3_bdd_computation import bdd_reachable, compare_methods, extract_markings, print_all_markings_bdd
from pathlib import Path
import pytest

from pyeda.inter import *


def test_001():
    base_dir = Path(__file__).parent.parent / "data" / "pnml"
    pn = PetriNet.from_pnml(str(base_dir / "phylosopher.pnml"))
    compare_methods(pn)

def test_002():
    base_dir = Path(__file__).parent.parent / "data" / "pnml"
    pn = PetriNet.from_pnml(str(base_dir / "deadlock1.pnml"))
    compare_methods(pn)


