import numpy as np

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def is_symbol_in_range(input_matrix, row, start_range, end_range):
    for j_p in range(start_range, end_range + 1):
        if input_matrix[row][j_p] == -2:
            return True
                
def extract_int_from_positions(input_matrix, positions):
    number_concatenated = ''
    for position in positions:
        number_str = str(input_matrix[position[0]][position[1]])
        number_concatenated += number_str
    return int(number_concatenated)

def is_symbol_around_number(input_matrix, matrix_shape, position):
    i = position[0]
    j = position[1]
    max_j = matrix_shape[0] - 1
    max_i = matrix_shape[1] - 1
    start_j = j - 1 if j > 0 else 0
    end_j = j + 1 if j < max_j else max_j

    if input_matrix[i][start_j] == -2 or input_matrix[i][end_j] == -2:
        return True

    if i == 0:
        return is_symbol_in_range(input_matrix, i + 1, start_j, end_j)
    elif 0 < i < max_i - 1:
        return is_symbol_in_range(input_matrix, i + 1, start_j, end_j) or is_symbol_in_range(input_matrix, i - 1, start_j, end_j)
    else:
        return is_symbol_in_range(input_matrix, i - 1, start_j, end_j)

def check_for_symbol_around_number_positions(input_matrix, number_positions):
    for number_position in number_positions:
        if is_symbol_around_number(input_matrix, input_matrix.shape, number_position):
            return extract_int_from_positions(input_matrix, number_positions)
    return 0

with open("D:\\repos\\AdventOfCode\\Day3\\input.txt", mode="r") as file:
    lines = file.readlines()
    x = len(lines[0]) - 1
    y = len(lines)
    input_matrix = np.zeros(shape=(x,y), dtype=int)
    current_row = 0
    for line in lines:
        current_column = 0
        for c in line.strip():
            if c in numbers:
                input_matrix[current_row][current_column] = int(c)
            elif c == '.':
                input_matrix[current_row][current_column] = -1
            else:
                input_matrix[current_row][current_column] = -2 

            current_column += 1
        current_row += 1
    print(input_matrix)

    numbers_to_sum = []
    for i in range(0, y):
        number_positions = []
        for j in range(0, x):
            number_to_add = 0
            if input_matrix[i][j] >= 0:
                number_positions.append((i,j))
            elif input_matrix[i][j] < 0:
                number_to_add = check_for_symbol_around_number_positions(input_matrix, number_positions)
                number_positions = []
            if j == x - 1 and len(number_positions) > 0:
                number_to_add = check_for_symbol_around_number_positions(input_matrix, number_positions)
                number_positions = []
            if number_to_add > 0:
                numbers_to_sum.append(number_to_add)
    print(numbers_to_sum)
    print(f"Output: {sum(numbers_to_sum)}")
    