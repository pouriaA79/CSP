import itertools
import os
import re
from typing import Dict, List, Optional

import numpy as np

from csp import Constraint, CSP

index = 2


class BinaryPuzzleConstraint(Constraint[str, str]):
    def __init__(self, element1: str, element2: str) -> None:
        super().__init__([element1, element2])
        self.element1: str = element1
        self.element2: str = element2

    def satisfied(self, assignment: Dict[str, str]) -> bool:
        global ans
        if self.element1 not in assignment or self.element2 not in assignment:
            ans = True
        elif assignment[self.element1] != assignment[self.element2]:
            ans = True
        else:
            ans = False

        if ans:
            first_puzzle, cols_num = read_file("puzzles/puzzle" + str(index) + ".txt")
            arrr = np.array(first_puzzle)
            puzzle_matrixx = arrr.reshape(cols_num, cols_num)
            pp = assignment_puzzle(assignment)
            cols_domain: Dict[str, List[str]] = {}
            for ii in range(0, cols_num):
                cols_domain["C" + str(ii)] = generateDomains(cols_num, int(cols_num / 2), puzzle_matrixx, "C" + str(ii))
            final = [False] * cols_num
            gone_col = ""
            d_num = -1
            for r in range(0, n):
                for x in cols_domain["C" + str(r)]:
                    if satisfy(pp[r], x):
                        final[r] = True
                        gone_col = x
                        d_num = r
                        break
                for t in range(0, n):
                    if t != d_num:
                        if gone_col in cols_domain["C" + str(t)]:
                            cols_domain["C" + str(t)].remove(gone_col)
            final_ans = all(final)
        else:
            return ans

        return final_ans


def assignment_puzzle(assignment):
    p = []
    lengths = [len(v) for v in assignment.values()]
    n = lengths[0]
    for t in range(0, n):
        p.append("-" * n)

    for k in assignment.keys():
        p[int(k[1])] = assignment[k]
    p_prime = []
    for i in range(0, n):
        col = []
        for j in range(0, n):
            col.append(p[j][i])
        p_prime.append(col)
    return p_prime


def satisfy(possible, pattern):
    s = True
    for g in range(0, len(possible)):
        if possible[g] != "-" and pattern[g] != possible[g]:
            s = False
            break
    return s


def read_file(file):
    file = open(file, 'r')
    first_line = file.readline()
    num, _ = first_line.split(" ")
    num = int(num)

    matrix = []
    for i in range(num):
        line = file.readline()
        row = re.split("\n| ", line)
        for j in range(num):
            matrix.append(row[j])

    return matrix, num


def generateDomains(n, k, p, v):
    result = []
    for bits in itertools.combinations(range(n), k):
        s = ['0'] * n
        for bit in bits:
            s[bit] = '1'
        if not next_each_other_constraint(s):
            if not same_to_input(s, p, v):
                result.append(''.join(s))
    return result


def next_each_other_constraint(element):
    discard = False
    for r in range(0, len(element) - 2):
        if element[r] == element[r + 1] and element[r + 1] == element[r + 2]:
            discard = True
            break
    return discard


def same_to_input(s, p, v):
    discard = False
    if v[0] == "R":
        for c in range(0, len(s)):
            if p[c][int(v[1])] != "-" and p[c][int(v[1])] != s[c]:
                discard = True
                break
    else:
        for c in range(0, len(s)):
            if p[int(v[1])][c] != "-" and p[int(v[1])][c] != s[c]:
                discard = True
                break
    return discard


if __name__ == "__main__":
    input_dir = "puzzles"
    inputs = os.listdir(input_dir)
    puzzle, n = read_file(input_dir + os.sep + inputs[index])
    arr = np.array(puzzle)
    puzzle_matrix = arr.reshape(n, n)
    variable: List[str] = []

    for i in range(0, n):
        variable.append(str("R" + str(i)))
    domain: Dict[str, List[str]] = {}
    for v in variable:
        domain[v] = generateDomains(n, int(n / 2), puzzle_matrix, v)
    csp: CSP[str, str] = CSP(variable, domain)
    for ac in range(0, n):
        for bc in range(ac + 1, n):
            csp.add_constraint(BinaryPuzzleConstraint(variable[ac], variable[bc]))

    solution: Optional[Dict[str, str]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        for i in variable[0: len(variable)]:
            print(i, "','".join(solution[i]))
