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

        if i != k and "-" not in matrix[k] and '-' not in str_row and str_row == matrix[k]:
            return True
        if j != k and "-" not in matrix[:, k] and '-' not in str_col and str_col == matrix[:, k]:
            return True
    return False


if __name__ == "__main__":
    file_names = "puzzle0.txt"
    puzzle_matrix, num_columns = read_file(file_names)
    arr = np.array(puzzle_matrix)
    puzzle_matrix = arr.reshape(num_columns, num_columns)
    print(puzzle_matrix[1])
    # if "2" in puzzle_matrix[:, 1] : print(5)
