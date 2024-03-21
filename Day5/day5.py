from parse import parse_file, extract_integers
import re

map_chain = ['seed-to-soil', 'soil-to-fertilizer', 'fertilizer-to-water', 'water-to-light',
             'light-to-temperature', 'temperature-to-humidity', 'humidity-to-location']


class RangeEncodedMap():
    def __init__(self, ranges) -> None:
        self.ranges = ranges
        self.ranges.sort(key=lambda elem: elem[1])

    def __repr__(self) -> str:
        return f'{self.ranges}'

    def __call__(self, source_element):
        for (destination_range_start, source_range_start, range_length) in self.ranges:
            if source_element >= source_range_start and source_element < source_range_start + range_length:
                return destination_range_start + source_element - source_range_start
        return source_element

    def map_range(self, start, length):
        resulting_ranges = []
        current_source_element = start
        elements_left = length
        while current_source_element < start + length:
            current_source_element_changed = False
            for (destination_range_start, source_range_start, range_length) in self.ranges:
                if current_source_element < source_range_start:
                    resulting_ranges.append((current_source_element, min(
                        source_range_start - current_source_element, elements_left)))
                    current_source_element = source_range_start
                    elements_left -= source_range_start - current_source_element
                    current_source_element_changed = True
                    break
                elif current_source_element < source_range_start + range_length:
                    destination_element = destination_range_start + \
                        current_source_element - source_range_start
                    mapped_range_length = min(
                        source_range_start + range_length - current_source_element, elements_left)
                    resulting_ranges.append(
                        (destination_element, mapped_range_length))
                    current_source_element = source_range_start + range_length
                    elements_left -= mapped_range_length
                    current_source_element_changed = True
                    break
            if not current_source_element_changed:
                resulting_ranges.append(
                    (current_source_element, elements_left))
                break
        return resulting_ranges


def parse_input(filename):
    lines = parse_file(filename)
    seeds = extract_integers(lines[0])
    maps = {}
    current_ranges = []
    current_map_title = 'seed-to-soil'
    for line in lines[3:]:
        if line == '':
            continue

        m = re.match('([a-z\-]+) map', line)
        if m is None:
            current_ranges.append(extract_integers(line))
        else:
            maps[current_map_title] = RangeEncodedMap(current_ranges)
            current_ranges = []
            current_map_title = m.group(1)
    maps[current_map_title] = RangeEncodedMap(current_ranges)
    return (seeds, maps)


def get_seed_location(seed, maps):
    cur = seed
    for map_name in map_chain:
        cur = maps[map_name](cur)
    return cur


def solve_part1(filename):
    (seeds, maps) = parse_input(filename)
    locations = list(map(lambda seed: get_seed_location(seed, maps), seeds))
    print(min(locations))


def solve_part2(filename):
    (seeds, maps) = parse_input(filename)
    current_ranges = [(seeds[2*i], seeds[2*i + 1])
                      for i in range(len(seeds)//2)]
    for map_name in map_chain:
        next_ranges = []
        for (start, length) in current_ranges:
            next_ranges.extend(maps[map_name].map_range(start, length))
        current_ranges = next_ranges
    print(min(current_ranges, key=lambda r: r[0]))


if __name__ == '__main__':
    solve_part2('input')
