import re


def read_file(name):
    file = open(name, 'r')
    s = file.readline()
    num_rows, num_columns = s.split(" ")
    num_rows, num_columns = int(num_rows), int(num_columns)

    matrix = [['0' for i in range(num_columns)] for j in range(num_rows)]
    for i in range(num_rows):
        str = file.readline()
        row = re.split("\n| ", str)
        for j in range(num_columns):
            if row[j] != '0':
                matrix[i][j] = row[j]

    return matrix


if __name__ == "__main__":
    file_names = "puzzle0.txt"
    puzzle_matrix = read_file(file_names)
    # print(puzzle_matrix)
