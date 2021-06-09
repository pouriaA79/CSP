import re

import numpy as np


def read_file(name):
    file = open(name, 'r')
    s = file.readline()
    num_rows, num_columns = s.split(" ")
    num_rows, num_columns = int(num_rows), int(num_columns)

    matrix = []
    for i in range(num_rows):
        str = file.readline()
        row = re.split("\n| ", str)
        for j in range(num_columns):
            matrix.append(row[j])

    return matrix, num_columns


def constraints_row(matrix, i, j, num, num_columns):
    num_one = 0
    num_zero = 0
    for k in range(num_columns):
        if matrix[i][k] == "1" and k != j:
            num_one += 1
        elif matrix[i][k] == "0" and k != j:
            num_zero += 1

    if num == 1:
        if num_one + 1 > num_columns / 2:
            return True
    elif num == 0:
        if num_zero + 1 > num_columns / 2:
            return True

    return False


def constraints_col(matrix, j, i, num, num_columns):
    num_one = 0
    num_zero = 0
    for k in range(num_columns):
        if matrix[k][j] == "1" and k != i:
            num_one += 1
        elif matrix[k][j] == "0" and k != i:
            num_zero += 1

    if num == 1:
        if num_one + 1 > num_columns / 2:
            return True
    elif num == 0:
        if num_zero + 1 > num_columns / 2:
            return True

    return False


def constraints_repeat(matrix, j, i, num, num_columns):
    if j - 2 >= 0 and matrix[i][j - 1] == str(num) and matrix[i][j - 2] == str(num):
        return True
    elif j + 2 <= num_columns - 1 and matrix[i][j + 1] == str(num) and matrix[i][j + 2] == str(num):
        return True
    elif j - 1 >= 0 and j + 1 <= num_columns - 1 and matrix[i][j - 1] == str(num) and matrix[i][j + 1] == str(num):
        return True
    elif i - 2 >= 0 and matrix[i - 1][j] == str(num) and matrix[i - 2][j] == str(num):
        return True
    elif i + 2 <= num_columns - 1 and matrix[i + 1][j] == str(num) and matrix[i + 2][j] == str(num):
        return True
    elif i + 1 <= num_columns - 1 and i - 1 >= 0 and matrix[i + 1][j] == str(num) and matrix[i - 1][j] == str(num):
        return True
    else:
        return False


def constraints_str(matrix, i, j, num, num_columns):
    row = matrix[i]
    col = matrix[:, j]
    str_col = ''
    str_row = ''

    for k in range(num_columns):
        if k != j:
            str_col += col[k]
        else:
            str_col += str(num)
        if k != i:
            str_row += row[k]
        else:
            str_row += str(num)

    for k in range(num_columns):

        if i != k and ("-" not in matrix[k] and '-' not in str_row and (str_row == matrix[k]).all()):
            return True
        if j != k and ("-" not in matrix[:, k] and '-' not in str_col and (str_col == matrix[:, k]).all()):
            return True
    return False


def get_possible_values(puzzle, num, i, j):
    number = 0
    domain = []
    for k in range(2):
        if constraints_row(puzzle, i, j, k, num):
            continue
        elif constraints_col(puzzle, i, j, k, num):
            continue
        elif constraints_repeat(puzzle, i, j, k, num):
            continue
        elif constraints_str(puzzle, i, j, k, num):
            continue
        else:
            domain.append(k)
            number += 1
    return number, domain


def forwardcheking(puzzle, num):
    mrv_values = {}
    num_mrv = 0
    flag = False
    for i in range(num):
        for j in range(num):
            if puzzle[i][j] == '-':
                tmp, domain = get_possible_values(puzzle, num, i, j)
                if len(domain) == 0:
                    flag = True
                mrv_values.setdefault(num_mrv, []).append(tmp)
                mrv_values.setdefault(num_mrv, []).append(domain)
                mrv_values.setdefault(num_mrv, []).append((i, j))
                num_mrv += 1
    sort = sorted(mrv_values.items(), key=lambda x: x[1], reverse=False)
    print(sort)
    return sort, flag


def MRV(puzzle, value, use):
    use.append(value[0])
    i, j = value[0][1][2]
    # print(value[0][1][1][0], i ,j)
    puzzle[i][j] = str(value[0][1][1][0])
    print(puzzle)
    value.remove(value[0])

    return value, puzzle, use


if __name__ == "__main__":
    file_names = "puzzle0.txt"
    used = []
    # wrong = {}
    puzzle_matrix, num_columns = read_file(file_names)
    arr = np.array(puzzle_matrix)
    puzzle_matrix = arr.reshape(num_columns, num_columns)
    values, flag_end = forwardcheking(puzzle_matrix, num_columns)

    while not flag_end:
        v, puzzle_matrix, u = MRV(puzzle_matrix, values, used)
        values, flag_end = forwardcheking(puzzle_matrix, num_columns)
