
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

with open("input.txt", mode="r") as file:
    lines = file.readlines()
    sum = 0
    i = 0
    for line in lines:
        number_1 = None
        number_2 = None
        for c in line:
            if c in numbers:
                number_1 = c
                break
        for c in reversed(line):
            if c in numbers:
                number_2 = c
                break
        
        if number_1 and number_2:
            number_to_add = int(f"{number_1}{number_2}")
            print(f"{i}: {number_to_add}, number_1: {number_1}, number_2: {number_2}")
            sum += number_to_add
        i += 1
    
    print(sum)

