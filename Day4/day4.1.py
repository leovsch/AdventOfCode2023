def add_to_copy_amounts(copies, card_number):
    if card_number in copies.keys():
        copies[card_number] += 1
    else: 
        copies[card_number] = 1

with open("input.txt", mode="r") as file:
    lines = file.readlines()
    total_score = 0
    copy_amounts = {}
    for line in lines:
        input_card = line.split("|")
        drawn_numbers_str = input_card[0].strip()
        my_numbers_str = input_card[1].strip()
        winning_numbers = [int(x.strip()) for x in drawn_numbers_str[drawn_numbers_str.index(":") + 1:].split(" ") if x != '']
        my_numbers = [int(x.strip()) for x in my_numbers_str.split(" ") if x != '']
        card_number = int(line[line.index(" ") + 1:line.index(":")])
        score = 0
        add_to_copy_amounts(copy_amounts, card_number)
        for my_number in my_numbers:
            if my_number in winning_numbers:
                if score == 0:
                    score = 1
                else:
                    score += 1
        for j in range(0, copy_amounts[card_number]):
            for i in range(card_number + 1, card_number + score + 1):
                if i <= len(lines):
                    add_to_copy_amounts(copy_amounts, i)

    print(sum(copy_amounts.values()))