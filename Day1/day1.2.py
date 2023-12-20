
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
numbers_text = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
numbers_text_reversed = [number_text[::-1] for number_text in numbers_text]

def get_number_value(c, number_str, reversed):
    if c in numbers:
        return c

    if reversed:
        for number_str_val in numbers_text_reversed:
            if number_str_val in number_str:
                return numbers_text_reversed.index(number_str_val)
    else:        
        for number_str_val in numbers_text:
            if number_str_val in number_str:
                return numbers_text.index(number_str_val)
    
    return -1

def get_number_from_line(line, reversed):
    number_str = ""
    for c in line:
        number_str += c
        number_str = number_str.strip()
        extracted_number = get_number_value(c, number_str, reversed)
        if extracted_number != -1:
            return extracted_number
    return None


with open("input.txt", mode="r") as file:
    lines = file.readlines()
    sum = 0
    i = 0
    for line in lines:
        line_lower = line.lower()
        number_1 = get_number_from_line(line_lower, False)
        number_2 = get_number_from_line(reversed(line_lower), True)
        
        if number_1 and number_2:
            number_to_add = int(f"{number_1}{number_2}")
            print(f"{i}: {number_to_add}, number_1: {number_1}, number_2: {number_2}")
            sum += number_to_add
        i += 1
    
    print(sum)

