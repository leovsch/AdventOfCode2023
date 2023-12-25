
from multiprocessing.pool import ThreadPool


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
    dictionary[(source_range_target, source_range_target + range_value - 1)] = (destination_range_target, destination_range_target + range_value - 1)

def get_value_from_mapping(dictionary, key):
    for source_range in dictionary.keys():
        if source_range[0] <= key <= source_range[1]:
            index_in_range = key - source_range[0]
            return dictionary[source_range][0] + index_in_range
    return key

def get_source_for_value(dictionary, value):
    for source_range in dictionary.keys():
        if dictionary[source_range][0] <= value <= dictionary[source_range][1]:
            return source_range[0] + (value - dictionary[source_range][0])
    return value

def get_min_location_seed_range(seed_range):
    locations = []
    for seed in range(seed_range[0], seed_range[1]):
        soil = get_value_from_mapping(seed_to_soil, seed)
        fertilizer = get_value_from_mapping(soil_to_fertilizer, soil)
        water = get_value_from_mapping(fertilizer_to_water, fertilizer)
        light = get_value_from_mapping(water_to_light, water)
        temperature = get_value_from_mapping(light_to_temperature, light)
        humidity = get_value_from_mapping(temperature_to_humidity, temperature)
        location = get_value_from_mapping(humidity_to_location, humidity)
        locations.append(location)
    return min(locations)

def get_min_dest_range_in_value_ranges_dictionary(dictionary):
    min_value = min([dictionary[source_range][0] for source_range in dictionary.keys()])
    return (0, [dictionary[source_range] for source_range in dictionary.keys() if dictionary[source_range][0] == min_value][0][1])

def get_source_range_containing_range(dictionary, range):
    min_value_range = range[0]
    max_value_range = range[1]
    min_value_return_val = None
    max_value_return_val = None
    for source_range in dictionary.keys():
        min_value_source_range = dictionary[source_range][0]
        max_value_source_range = dictionary[source_range][1]
        if min_value_source_range <= min_value_range <= max_value_source_range:
            min_value_return_val = source_range[0] + (min_value_range - min_value_source_range)
        if max_value_range <= max_value_source_range:
            max_value_return_val = source_range[1] + (max_value_source_range - max_value_range)
        if max_value_return_val != None and min_value_return_val != None:
            break
    return (min_value_return_val, max_value_return_val) if min_value_return_val != None and max_value_return_val != None else range


with open("/home/leo/repos/AdventOfCode2023/Day5/input.txt", mode="r") as file:
    lines = file.readlines()
    line_with_seeds = lines[0]
    seed_range_numbers = [int(seed_number.strip()) for seed_number in line_with_seeds[line_with_seeds.index(":") + 1:].split(" ") if seed_number != '']
    seed_ranges = [(seed_range_numbers[i], seed_range_numbers[i] + seed_range_numbers[i + 1] - 1) for i in range(0, len(seed_range_numbers)) if i % 2 == 0]
    parse_bools = ParseBools()
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


    # max_location_value_within_ranges = get_max_dest_value_from_range_dictionary(humidity_to_location)
    print("Computing min range...")

    min_location_range = sorted(humidity_to_location)[0]
    min_huminity_range = get_source_range_containing_range(humidity_to_location, min_location_range)
    min_temperature_range = get_source_range_containing_range(temperature_to_humidity, min_huminity_range)
    min_light_range = get_source_range_containing_range(light_to_temperature, min_temperature_range)
    min_water_range = get_source_range_containing_range(water_to_light, min_light_range)
    min_fertilizer_range = get_source_range_containing_range(fertilizer_to_water, min_water_range)
    min_soil_range = get_source_range_containing_range(soil_to_fertilizer, min_fertilizer_range)
    min_seed_range = get_source_range_containing_range(seed_to_soil, min_soil_range)
    
    print(f"Found min seed range: {min_seed_range}")


    seed_ranges_sorted = sorted(seed_ranges)
    min_seed_to_check = min_seed_range[0]
    max_seed_to_check = min_seed_range[1]
    seed_ranges_to_check = []
    max_seed_in_range = 0
    min_range_defined = False
    for seed_range in seed_ranges_sorted:
        if seed_range[0] <= min_seed_to_check <= seed_range[1] and max_seed_to_check > seed_range[1]:
            seed_ranges_to_check.append((min_seed_to_check, seed_range[1]))
            min_range_defined = True
        elif seed_range[0] >= min_seed_to_check and max_seed_to_check > seed_range[1]:
            seed_ranges_to_check.append(seed_range)
            min_range_defined = True
        elif seed_range[1] < max_seed_to_check and min_range_defined:
            seed_ranges_to_check.append(seed_range)
        elif max_seed_to_check <= seed_range[1] and min_range_defined:
            seed_ranges_to_check.append((seed_range[0], max_seed_to_check))
    
    print(f"Found {len(seed_ranges_to_check)} seed range to check")
    print(f"Sorted seed ranges: {seed_ranges_sorted}")
    print(f"Found seed ranges: {seed_ranges_to_check}")
    print(f"Total seeds to check: {sum([seed_range[1] - seed_range[0] for seed_range in seed_ranges_to_check])}")
    print(f"Max seed in seed ranges: {seed_ranges_sorted[len(seed_ranges_sorted)-1][1]}" )
    pool = ThreadPool(processes=8)
    min_locations = pool.map(get_min_location_seed_range, seed_ranges_to_check)
    print(f"Minimal location: {min(min_locations)}")

    