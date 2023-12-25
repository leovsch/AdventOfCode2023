
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
    i = 0
    for seed in range(seed_range[0], seed_range[1]):
        if i % 1000000 == 0 and i > 0:
            print(f"1 million done for range {seed_range}")
        soil = get_value_from_mapping(seed_to_soil, seed)
        fertilizer = get_value_from_mapping(soil_to_fertilizer, soil)
        water = get_value_from_mapping(fertilizer_to_water, fertilizer)
        light = get_value_from_mapping(water_to_light, water)
        temperature = get_value_from_mapping(light_to_temperature, light)
        humidity = get_value_from_mapping(temperature_to_humidity, temperature)
        location = get_value_from_mapping(humidity_to_location, humidity)
        locations.append(location)
        i += 1
    return min(locations)

def range_fully_contained(range_a, range_b):
    return range_b[0] <= range_a[0] <= range_b[1] and range_b [0] <= range_a[1] <= range_b[1]

def range_fully_uncontained_left(range_a, range_b):
    return range_a[1] < range_b[0]

def range_fully_uncontained_right(range_a, range_b):
    return range_a[0] > range_b[1]

def range_fully_uncontained(range_a, range_b):
    return range_fully_uncontained_left(range_a, range_b) or range_fully_uncontained_right(range_a, range_b)

def range_partly_contained_left(range_a, range_b):
    return (range_b[0] <= range_a[1] <= range_b[1] and range_a[0] < range_b[1])

def range_partly_contained_right(range_a, range_b):
    return (range_b[0] <= range_a[0] <= range_b[1] and range_a[1] > range_b[1])

def range_partly_contained(range_a, range_b):
    return range_partly_contained_left(range_a, range_b) or range_partly_contained_right(range_a, range_b)

def extract_intersection_interval(range_a, range_b):
    if range_partly_contained_left(range_a, range_b):
        return (range_b[0], range_a[1])
    if range_partly_contained_right(range_a, range_b):
        return (range_a[0], range_b[1])

def extract_difference_interval(range_a, range_b):
    if range_b[0] == range_b[1] and (range_a[0] == range_b[0]):
        return (range_a[0] + 1, range_a[1])
    if range_b[0] == range_b[1] and (range_a[1] == range_b[0]):
        return (range_a[0], range_a[1] - 1)
    if range_partly_contained_left(range_a, range_b):
        return (range_a[0], range_b[0] - 1)
    if range_partly_contained_right(range_a, range_b):
        return (range_b[1] + 1, range_a[1])

def get_source_ranges_containing_range(dictionary, range, i):
    if i < len(dictionary):
        value_ranges_sorted = sorted(dictionary.values())
        small_range = value_ranges_sorted[i]
        if range_fully_contained(range, small_range):
            return [(get_source_for_value(dictionary, range[0]), get_source_for_value(dictionary, range[1]))]
    
        if range_fully_uncontained(range, small_range):
            i += 1
            return get_source_ranges_containing_range(dictionary, range, i)
        
        if range_partly_contained(range, small_range):
            intersection_range = extract_intersection_interval(range, small_range)
            difference_range = extract_difference_interval(range, small_range)
            ret_val = [(get_source_for_value(dictionary, intersection_range[0]), get_source_for_value(dictionary, intersection_range[1]))]
            i += 1
            ret_val.extend(get_source_ranges_containing_range(dictionary, difference_range, i))
            return ret_val
    return [range]    

def extract_potential_min_ranges(dictionary, ranges):
    ret_val = []
    for min_range in ranges:
        ret_val.extend(get_source_ranges_containing_range(dictionary, min_range, 0))
    return ret_val

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


    print(f"Seed to soil: {seed_to_soil}")
    print(f"Soil to fertilizer: {soil_to_fertilizer}")
    print(f"Fertilizer to water: {fertilizer_to_water}")
    print(f"Water to light: {water_to_light}")
    print(f"light to temperature: {light_to_temperature}")
    print(f"Temperatur to humidity: {temperature_to_humidity}")
    print(f"Humidity to location: {humidity_to_location}")
    print("Computing min range...")

    sorted_humidity_to_location = sorted(humidity_to_location)

    location_index = 0
    step_size = 1000000
    step_start = 0
    max_step_end = sorted_humidity_to_location[location_index][0]
    step_end = step_size
    min_location_range = (step_start, step_end)
    while step_end <= max_step_end:
        min_huminity_ranges = get_source_ranges_containing_range(humidity_to_location, min_location_range, 0)
        min_temperature_ranges = extract_potential_min_ranges(temperature_to_humidity, min_huminity_ranges)
        min_light_ranges = extract_potential_min_ranges(light_to_temperature, min_temperature_ranges)
        min_water_ranges = extract_potential_min_ranges(water_to_light, min_light_ranges)
        min_fertilizer_ranges = extract_potential_min_ranges(fertilizer_to_water, min_water_ranges)
        min_soil_ranges = extract_potential_min_ranges(soil_to_fertilizer, min_fertilizer_ranges)
        min_seed_ranges = extract_potential_min_ranges(seed_to_soil, min_soil_ranges)

        seed_ranges_sorted = sorted(seed_ranges)
        min_seed_ranges_sorted = sorted(min_seed_ranges)
        to_compute = []
    
        for seed_range in seed_ranges_sorted:
            to_remove = []
            for min_seed_range in min_seed_ranges_sorted:
                if range_fully_uncontained_left(min_seed_range, seed_range):
                    to_remove.append(min_seed_range)
                elif range_fully_contained(min_seed_range, seed_range):
                    to_compute.append(min_seed_range)
                elif range_partly_contained(min_seed_range, seed_range):
                    to_compute.append(extract_intersection_interval(min_seed_range, seed_range))
            for min_seed_range in to_remove:
                min_seed_ranges_sorted.remove(min_seed_range)
    
        seed_ranges_to_check = to_compute

        if len(to_compute) > 0:        
            print(f"Found {len(seed_ranges_to_check)} seed range to check")
            print(f"Sorted seed ranges: {seed_ranges_sorted}")
            print(f"Found seed ranges: {seed_ranges_to_check}")
            print(f"Total seeds to check: {sum([seed_range[1] - seed_range[0] for seed_range in seed_ranges_to_check])}")
            print(f"Max seed in seed ranges: {seed_ranges_sorted[len(seed_ranges_sorted)-1][1]}" )
            pool = ThreadPool(processes=8)
            min_locations = pool.map(get_min_location_seed_range, seed_ranges_to_check)
            print(f"Minimal location: {min(min_locations)}")
            break

        if step_end > max_step_end:
            step_end = max_step_end
            step_start += step_size
        elif step_start + step_size > max_step_end:
            location_index += 1
            step_start = sorted_humidity_to_location[location_index][0]
            max_step_end = sorted_humidity_to_location[location_index][1]
            step_end = step_start + step_size
        else:
            step_start += step_size
            step_end += step_size
        min_location_range = (step_start, step_end)

    
        