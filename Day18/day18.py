import re
import numpy as np
from parse import parse_file
from trench import Trench

LEFT_TURN_MATRIX = np.array([[0, -1],
                             [1, 0]])
RIGHT_TURN_MATRIX = np.array([[0, 1],
                              [-1, 0]])
DIRECTION_CHARS = ['R', 'D', 'L', 'U']
CHAR_TO_DIRECTION = {'D': np.array((1, 0)),
                     'R': np.array((0, 1)),
                     'U': np.array((-1, 0)),
                     'L': np.array((0, -1))}


class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __repr__(self):
        return f'#{self.r:x}{self.g:x}{self.b:x}'

    def from_hex(hex_string):
        r = int(hex_string[:2], 16)
        g = int(hex_string[2:4], 16)
        b = int(hex_string[4:], 16)
        return Color(r, g, b)


def parse_line(line):
    match = re.match("([LRUD]) ([0-9]+) \(#([0-9a-f]{6})\)", line)
    return (match.group(1), int(match.group(2)))


def parse_line_part2(line):
    match = re.match("[LRUD] [0-9]+ \(#([0-9a-f]{6})\)", line)
    return (DIRECTION_CHARS[int(match.group(1)[5])], int(match.group(1)[:5], 16))


def solve_part1(filename):
    instructions = parse_file(filename, parse_line)
    trench = Trench()
    trench.follow_instructions(instructions)
    trench.print_trench()
    trench.fill_trench()
    trench.print_trench()
    print(np.count_nonzero(trench.trench))
    # perimeter = compute_trench_perimeter(instructions)
    # perimeter = fix_perimeter(perimeter)
    # print(compute_area_of_polygon(perimeter) / 4)


def solve_part2(filename):
    instructions = parse_file(filename, parse_line_part2)
    perimeter = compute_trench_perimeter(instructions)
    area = compute_area(perimeter, instructions)
    print(area)


def compute_trench_perimeter(instructions):
    current_point = np.array((0, 0))
    perimeter = [current_point.copy()]
    for (dir_char, step_size) in instructions:
        direction = CHAR_TO_DIRECTION[dir_char]
        current_point += step_size * direction
        perimeter.append(current_point.copy())
    perimeter.pop()
    return np.array(perimeter)


def corners(p):
    p = list(p)
    return zip([p[-1]] + p[:-1], p, p[1:] + [p[0]])


def compute_corrections(turn_directions, initial_correction):
    corrections = [np.array(initial_correction)]
    prev_turn = turn_directions[0]
    for turn in turn_directions[1:]:
        if prev_turn + turn == 0:
            corrections.append(corrections[-1])
        else:
            corrections.append((turn * LEFT_TURN_MATRIX).dot(corrections[-1]))
    return corrections


def is_oriented_counter_clockwise(perimeter):
    return compute_orientation(perimeter) > 0


def compute_orientation(perimeter):
    return np.sign(compute_twice_oriented_area(perimeter))


def compute_twice_oriented_area(perimeter):
    def segments(p):
        p = list(p)
        return zip(p, p[1:] + [p[0]])

    return sum(x0*y1 - x1*y0 for ((x0, y0), (x1, y1)) in segments(perimeter))


def compute_area_of_polygon(perimeter):
    return 0.5 * abs(compute_twice_oriented_area(perimeter))


def compute_area(perimeter, instructions):
    inner_area = compute_area_of_polygon(perimeter)
    perimeter_length = sum((step_size for (_, step_size) in instructions))
    return inner_area + perimeter_length//2 + 1


def compute_area_directly(instructions):
    area = 0
    perimeter = 0
    x, y = 0, 0
    for (direction, step_size) in instructions:
        (dy, dx) = CHAR_TO_DIRECTION[direction]
        dy, dx = step_size * dy, step_size * dx
        x, y = x + dx, y + dy
        perimeter += step_size
        area += x * dy
    return area + perimeter//2 + 1


if __name__ == '__main__':
    solve_part1('example')
    solve_part2('input')
