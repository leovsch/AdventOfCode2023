seed_to_soil = {}
soil_to_fertilizer = {}
fertilizer_to_water = {}
water_to_light = {}
light_to_temperature = {}
temperature_to_humidity = {}
humidity_to_location = {}

class ParseBools:   

    def __init__(self):
        self.parse_seed_to_soil = False
        self.parse_soil_to_fertilizer = False
        self.parse_fertilizer_to_water = False
        self.parse_water_to_light = False
        self.parse_light_to_temperature = False
        self.parse_temperature_to_humidity = False
        self.parse_humidity_to_location = False

    def reset_bools(self):
        self.parse_seed_to_soil = False
        self.parse_soil_to_fertilizer = False
        self.parse_fertilizer_to_water = False
        self.parse_water_to_light = False
        self.parse_light_to_temperature = False
        self.parse_temperature_to_humidity = False
        self.parse_humidity_to_location = False

def add_mapping_to_dictionary(dictionary, number_string):
    numbers = [int(number) for number in number_string.split(" ")]
    destination_range_target = numbers[0]
    source_range_target = numbers[1]
    range_value = numbers[2]
    dictionary[(source_range_target, source_range_target + range_value)] = (destination_range_target, destination_range_target + range_value)

def get_value_from_mapping(dictionary, key):
    for source_range in dictionary.keys():
        if source_range[0] <= key <= source_range[1]:
            index_in_range = key - source_range[0]
            return dictionary[source_range][0] + index_in_range
    return key

with open("input.txt", mode="r") as file:
    lines = file.readlines()
    line_with_seeds = lines[0]
    seeds = [int(seed_number.strip()) for seed_number in line_with_seeds[line_with_seeds.index(":") + 1:].split(" ") if seed_number != '']
    parse_bools = ParseBools()
    locations = []
    for line in lines[1:]:
        clean_line = line.strip()
        if clean_line == 'seed-to-soil map:':
            parse_bools.reset_bools()
            parse_bools.parse_seed_to_soil = True
        elif clean_line == 'soil-to-fertilizer map:':
            parse_bools.reset_bools()
            parse_bools.parse_soil_to_fertilizer = True
        elif clean_line == 'fertilizer-to-water map:':
            parse_bools.reset_bools()
            parse_bools.parse_fertilizer_to_water = True
        elif clean_line == 'water-to-light map:':
            parse_bools.reset_bools()
            parse_bools.parse_water_to_light = True
        elif clean_line == 'light-to-temperature map:':
            parse_bools.reset_bools()
            parse_bools.parse_light_to_temperature = True        
        elif clean_line == 'temperature-to-humidity map:':
            parse_bools.reset_bools()
            parse_bools.parse_temperature_to_humidity = True
        elif clean_line == 'humidity-to-location map:':
            parse_bools.reset_bools()
            parse_bools.parse_humidity_to_location = True
        elif clean_line != '':
            if parse_bools.parse_seed_to_soil:
                add_mapping_to_dictionary(seed_to_soil, clean_line)
            elif parse_bools.parse_soil_to_fertilizer:
                add_mapping_to_dictionary(soil_to_fertilizer, clean_line)
            elif parse_bools.parse_fertilizer_to_water:
                add_mapping_to_dictionary(fertilizer_to_water, clean_line)
            elif parse_bools.parse_water_to_light:
                add_mapping_to_dictionary(water_to_light, clean_line)
            elif parse_bools.parse_light_to_temperature:
                add_mapping_to_dictionary(light_to_temperature, clean_line)
            elif parse_bools.parse_temperature_to_humidity:
                add_mapping_to_dictionary(temperature_to_humidity, clean_line)
            elif parse_bools.parse_humidity_to_location:
                add_mapping_to_dictionary(humidity_to_location, clean_line)
        
    for seed in seeds:
        soil = get_value_from_mapping(seed_to_soil, seed)
        fertilizer = get_value_from_mapping(soil_to_fertilizer, soil)
        water = get_value_from_mapping(fertilizer_to_water, fertilizer)
        light = get_value_from_mapping(water_to_light, water)
        temperature = get_value_from_mapping(light_to_temperature, light)
        humidity = get_value_from_mapping(temperature_to_humidity, temperature)
        location = get_value_from_mapping(humidity_to_location, humidity)
        locations.append(location)

    print(f"closest location: {min(locations)}")
        