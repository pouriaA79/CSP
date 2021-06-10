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


def constraints_row(matrix, i,j, num, num_columns):
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


def constraints_col(matrix, i,j, num, num_columns):
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


def constraints_repeat(matrix, i,j, num, num_columns):
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
    # print(row)
    for k in range(num_columns):
        if k != i:
            str_col += col[k]
        else:
            str_col += str(num)
        if k != j:
            str_row += row[k]
        else:
            str_row += str(num)

    for k in range(num_columns):
        # print(i, j, num)
        if i != k and "-" not in "".join(matrix[k]) and '-' not in str_row and str_row == "".join(matrix[k]):
            return True
        if j != k and "-" not in "".join(matrix[:, k]) and '-' not in str_col and str_col == "".join(matrix[:, k]):
            return True
    # print(i, j, num)
    return False


def get_possible_values(puzzle, num, i, j):
    number = 0
    domain = []
    # print(puzzle ,num ,i ,j)
    for k in range(2):
        if constraints_row(puzzle, i, j, k, num):
            # print(5, k)
            continue

        elif constraints_col(puzzle, i, j, k, num):
            # print(6, k)
            continue
        elif constraints_repeat(puzzle, i, j, k, num):
            # print(constraints_repeat(puzzle, 3, 0, 0, num))
            # print(99, k, i, j)
            continue
        elif constraints_str(puzzle, i, j, k, num):
            # print(8, k)
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
    # print(sort)
    return sort, flag


def MRV(puzzle, value, use, number,j):
    numm = 0
    # print(value)
    # print("=========")
    if j != 0:
        for i in range(len(value)):
            if number == value[i][0]:
                if i + 1 == len(value):
                    return True, value, puzzle, use
                else:
                    # print(value[i + 1])
                    use.append(value[i + 1])
                    numm = i + 1

    else:
        use.append(value[0])

    i, j = value[numm][1][2]
    # print(value[0][1][1][0], i ,j)
    # print(value[0][1])
    puzzle[i][j] = str(value[numm][1][1][0])
    print(puzzle)
    value.remove(value[numm])

    return False, value, puzzle, use


def backtracking(name):
    puzzle_matrix, num_columns = read_file(name)
    arr = np.array(puzzle_matrix)
    puzzle_matrix = arr.reshape(num_columns, num_columns)
    values, flag_end = forwardcheking(puzzle_matrix, num_columns)
    u = []
    end = False
    last_num = 0
    j = 0
    for i in range(100000):
        flag_end = False

        while not flag_end:

            if '-' not in puzzle_matrix:
                print("done")
                end = True
                break
            if j == 0 and i != 0:
                print(j)
                j += 1
                flag_end, v, puzzle_matrix, u = MRV(puzzle_matrix, values, u, last_num, j)
                if flag_end:
                    break
            else:
                flag_end, v, puzzle_matrix, u = MRV(puzzle_matrix, values, u, 0, 0)
            values, flag_end = forwardcheking(puzzle_matrix, num_columns)

            # print(u)
            # print(4)
        if end:
            print(puzzle_matrix)
            break
        else:
            print(values)
            print("====")
            j = 0
            # print(u)
            # print(65465)
            # print(u[-1][1][2][0])
            puzzle_matrix[u[-1][1][2][0]][u[-1][1][2][1]] = '-'
            last_num = u[-1][0]
            values, flag_end = forwardcheking(puzzle_matrix, num_columns)
            print(values)
            print(last_num)
            print(99999999999999999999999999999999999999999999999999999)
            u.pop(-1)


if __name__ == "__main__":
    file_names = "puzzle5.txt"
    backtracking(file_names)
