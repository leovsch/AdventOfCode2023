from dataclasses import dataclass
from typing import List

@dataclass
class CubeSet:
    nr_red : int    
    nr_blue : int    
    nr_green : int

    def print_cube_set(self):
        print(f"nr_red: {self.nr_red}, nr_green: {self.nr_green}, nr_blue: {self.nr_blue}")

@dataclass
class Game:
    game_nr : int
    sets : List[CubeSet]

    def print_game(self):
        print(f"Game Nr: {self.game_nr}")
        for set in self.sets:
            set.print_cube_set()

def get_nr_from_set(cube_set_value_str : str, color : str):
    if color in cube_set_value_str:
        return int(cube_set_value_str[0:cube_set_value_str.index(" ")])
    return 0

def parse_game(line : str) -> Game:
    game_number = int(line[line.index(" "):line.index(":")].strip())
    game_input = line[line.index(":")+1:]
    game_input = game_input.strip()
    cube_sets = game_input.split(";")
    game_sets = []
    for cube_set in cube_sets:
        nr_blue = 0
        nr_red = 0
        nr_green = 0
        for cube_set_value in cube_set.split(","):
            cube_set_value_str = cube_set_value.strip().lower()
            nr_blue += get_nr_from_set(cube_set_value_str, 'blue')
            nr_red += get_nr_from_set(cube_set_value_str, 'red')
            nr_green += get_nr_from_set(cube_set_value_str, 'green')
        game_sets.append(CubeSet(nr_red, nr_blue, nr_green))
    return Game(game_number, game_sets)
            
max_nr_red = 12
max_nr_green = 13
max_nr_blue = 14

with open("input.txt", mode="r") as file:
    lines = file.readlines()
    sum = 0
    for line in lines:
        game = parse_game(line.strip())
        max_red = max([set.nr_red for set in game.sets])
        max_green = max([set.nr_green for set in game.sets])
        max_blue = max([set.nr_blue for set in game.sets])
        power_of_game_set = max_red * max_green * max_blue
        sum += power_of_game_set
    print(f"Output: {sum}")

