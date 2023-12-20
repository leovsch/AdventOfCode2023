import numpy as np

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def is_star_in_range(input_matrix, row, start_range, end_range):
    for j_p in range(start_range, end_range + 1):
        if input_matrix[row][j_p] == -2:
            return [(row, j_p)]
    return []
                
def extract_int_from_positions(input_matrix, positions):
    number_concatenated = ''
    for position in positions:
        number_str = str(input_matrix[position[0]][position[1]])
        number_concatenated += number_str
    return int(number_concatenated)

def is_star_around_number(input_matrix, matrix_shape, position):
    i = position[0]
    j = position[1]
    max_j = matrix_shape[0] - 1
    max_i = matrix_shape[1] - 1
    start_j = j - 1 if j > 0 else 0
    end_j = j + 1 if j < max_j else max_j
    ret_val = []
    if input_matrix[i][start_j] == -2:
        return [(i, start_j)]
    elif input_matrix[i][end_j] == -2:
        return [(i, end_j)]

    if i == 0:
        return is_star_in_range(input_matrix, i + 1, start_j, end_j)
    elif 0 < i < max_i - 1:
        star_positions_above = is_star_in_range(input_matrix, i + 1, start_j, end_j)
        star_positions_below = is_star_in_range(input_matrix, i - 1, start_j, end_j)
        ret_val = star_positions_above + star_positions_below
        return ret_val
    else:
        return is_star_in_range(input_matrix, i - 1, start_j, end_j)

def extract_star_positions(input_matrix, number_positions):
    for number_position in number_positions:
        star_positions = is_star_around_number(input_matrix, input_matrix.shape, number_position)
        if len(star_positions) > 0:
            number = extract_int_from_positions(input_matrix, number_positions)
            return (number, star_positions)
    return None

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
            elif c == '*':
                input_matrix[current_row][current_column] = -2
            else:
                input_matrix[current_row][current_column] = -3 

            current_column += 1
        current_row += 1

    numbers_star_position_pairs = []
    for i in range(0, y):
        number_positions = []
        for j in range(0, x):
            number_star_positions_pair = None
            if input_matrix[i][j] >= 0:
                number_positions.append((i,j))
            elif input_matrix[i][j] < 0:
                number_star_positions_pair = extract_star_positions(input_matrix, number_positions)
                number_positions = []
            if j == x - 1 and len(number_positions) > 0:
                number_star_positions_pair = extract_star_positions(input_matrix, number_positions)
                number_positions = []
            if number_star_positions_pair != None:
                numbers_star_position_pairs.append(number_star_positions_pair)
    
    # print(numbers_star_position_pairs)

    numbers_to_sum = []
    for i in range(0, len(numbers_star_position_pairs)):
        number_i = numbers_star_position_pairs[i][0]
        star_positions_i = numbers_star_position_pairs[i][1]
        gear_ratio = number_i
        for j in range(i + 1, len(numbers_star_position_pairs)):            
            number_j = numbers_star_position_pairs[j][0]
            star_positions_j = numbers_star_position_pairs[j][1]
            for star_position in star_positions_j:
                if star_position in star_positions_i:
                    gear_ratio *= number_j
                    numbers_star_position_pairs[i][1].remove(star_position)
                    numbers_star_position_pairs[j][1].remove(star_position)
        if gear_ratio > number_i:
            numbers_to_sum.append(gear_ratio)

    print(f"Output: {sum(numbers_to_sum)}")
    