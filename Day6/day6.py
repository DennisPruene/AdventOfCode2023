from math import sqrt, ceil

times = [42, 68, 69, 85]
distances = [284, 1005, 1122, 1341]


def number_of_ways_record_can_be_beaten(max_time, record):
    max_hold_time = (max_time + sqrt(max_time**2 - 4*record)) / 2
    min_hold_time = record / max_hold_time
    max_hold_time_rounded = int(max_hold_time)
    min_hold_time_rounded = ceil(min_hold_time)
    if max_hold_time == float(max_hold_time_rounded):
        max_hold_time_rounded += 1
    if min_hold_time == float(min_hold_time_rounded):
        min_hold_time_rounded += 1
    return max_hold_time_rounded - min_hold_time_rounded + 1


def solve_part1():
    solution = 1
    for (max_time, record) in zip(times, distances):
        solution *= number_of_ways_record_can_be_beaten(max_time, record)
    print(solution)


def solve_part2():
    max_time = int(''.join(map(str, times)))
    record = int(''.join(map(str, distances)))
    print(number_of_ways_record_can_be_beaten(max_time, record))


if __name__ == '__main__':
    solve_part1()
    solve_part2()
