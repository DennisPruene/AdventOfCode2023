from parse import parse_file


def parse_input(filename):
    data = parse_file(filename)
    initialization_sequence = data[0].split(',')
    return initialization_sequence


def solve_part1(filename):
    initialization_sequence = parse_input(filename)
    print(sum(compute_hash(string) for string in initialization_sequence))


def solve_part2(filename):
    initialization_sequence = parse_input(filename)
    hashmap = [[[], []] for _ in range(256)]
    for string in initialization_sequence:
        if "-" in string:
            key = string[:-1]
            hash_value = compute_hash(key)
            if key in hashmap[hash_value][0]:
                i = hashmap[hash_value][0].index(key)
                hashmap[hash_value][0].pop(i)
                hashmap[hash_value][1].pop(i)
        else:
            (key, lens_value) = string.split('=')
            lens_value = int(lens_value)
            hash_value = compute_hash(key)
            if key in hashmap[hash_value][0]:
                hashmap[hash_value][1][hashmap[hash_value]
                                       [0].index(key)] = lens_value
            else:
                hashmap[hash_value][0].append(key)
                hashmap[hash_value][1].append(lens_value)
    print(hashmap)
    solution = 0
    for (box_index, (_, lenses)) in enumerate(hashmap):
        for (slot_index, lens) in enumerate(lenses):
            solution += (box_index + 1) * (slot_index + 1) * lens
    print(solution)


def compute_hash(string):
    current_hash = 0
    for char in string:
        current_hash += ord(char)
        current_hash *= 17
        current_hash %= 256
    return current_hash


if __name__ == '__main__':
    solve_part1('input')
    solve_part2('input')
