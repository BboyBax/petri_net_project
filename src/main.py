"""
main.py
Điểm bắt đầu của dự án Petri Net
Chủ đề: Symbolic and Algebraic Reasoning in Petri Nets
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.task1_parser import PetriNet
from src.task2_explicit_reachability import explicit_reachability, print_all_markings
from src.task3_symbolic_reachability import bdd_reachable, compare_methods
from src.task4_deadlock_detection import deadlock_reachable_marking
from src.task5_optimize_reachable_markings import max_reachable_marking
from src.utils import print_separator

from pathlib import Path
import argparse
import numpy as np 

def main():
    parser = argparse.ArgumentParser(description="Petri Net Analyzer")
    parser.add_argument("pnml_file", help="Link to file PNML")
    parser.add_argument("--task", type=int, choices=[1,2,3,4,5], required=True,
                        help="Choose task to run (1-5)")
    parser.add_argument("--c", nargs="+", type=int,
                        help="Vector hệ số c cho Task 5 (vd: --c 0 2 5 3)")
    args = parser.parse_args()

    pn = PetriNet.from_pnml(args.pnml_file)

    if args.task == 2:
        print(len(explicit_reachability(pn)))
    elif args.task == 3:
        compare_methods(pn)
    elif args.task == 4:
        bdd, R = bdd_reachable(pn)
        marking = deadlock_reachable_marking(pn, bdd, R)
        print(marking)
    elif args.task == 5:
        if args.c is None:
            print("Task 5 needs vector c. Please enter the amount --c")
        else:
            bdd, R = bdd_reachable(pn)
            c = np.array(args.c)
            marking, value = max_reachable_marking(pn.place_ids, R, c)

            print("Optimal marking:", marking)
            print("Optimal value:", value)

            assert value == max(np.dot(c, m) for m in explicit_reachability(pn))
    else:
        print("Read and check file pnml")
        errors = pn.validate()
        if errors:
            print("Validation errors found:")
            for e in errors:
                print(" -", e)
        else:
            print("Validation passed: Petri Net structure is consistent.")
            print(pn)

if __name__ == "__main__":
    main()
