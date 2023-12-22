with open("input.txt", mode="r") as file:
    lines = file.readlines()
    total_score = 0
    for line in lines:
        input_card = line.split("|")
        drawn_numbers_str = input_card[0].strip()
        my_numbers_str = input_card[1].strip()
        winning_numbers = [int(x.strip()) for x in drawn_numbers_str[drawn_numbers_str.index(":") + 1:].split(" ") if x != '']
        my_numbers = [int(x.strip()) for x in my_numbers_str.split(" ") if x != '']
        
        score = 0
        for my_number in my_numbers:
            if my_number in winning_numbers:
                if score == 0:
                    score = 1
                else:
                    score *= 2
        total_score += score
    
    print(total_score)
