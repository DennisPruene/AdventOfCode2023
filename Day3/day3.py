from parse import parse_file
from typing import List, Tuple
import re


class SchematicNumber:
    def __init__(self, value, x, y, length) -> None:
        self.value = value
        self.x = x
        self.y = y
        self.length = length

    def does_symbol_touch(self, x_sym, y_sym):
        return x_sym >= self.x - 1 and x_sym <= self.x + self.length \
            and y_sym >= self.y - 1 and y_sym <= self.y + 1

    def __repr__(self) -> str:
        return f'({self.value, self.x, self.y, self.length})'


def solve_part1(filename):
    schematic = parse_file(filename)
    numbers_by_line = extract_numbers(schematic)
    symbol_positions = extract_symbol_positions(schematic)
    solution = 0
    for (x, y) in symbol_positions:
        for line in range(max(0, y - 1), min(len(schematic), y + 2)):
            for number in numbers_by_line[line]:
                if number.does_symbol_touch(x, y):
                    solution += number.value
    print(solution)


def extract_numbers(schematic):
    numbers_by_line = []
    for (y, line) in enumerate(schematic):
        current_numbers = []
        for match in re.finditer('([0-9]+)', line):
            current_numbers.append(SchematicNumber(
                int(match.group()), match.start(), y, match.end() - match.start()))
        numbers_by_line.append(current_numbers)
    return numbers_by_line


def extract_symbol_positions(schematic):
    positions = []
    for (y, line) in enumerate(schematic):
        for match in re.finditer('[^0-9\.]', line):
            positions.append((match.start(), y))
    return positions


def extract_gear_positions(schematic):
    positions = []
    for (y, line) in enumerate(schematic):
        for match in re.finditer('\*', line):
            positions.append((match.start(), y))
    return positions


def solve_part2(filename):
    schematic = parse_file(filename)
    numbers_by_line = extract_numbers(schematic)
    gear_positions = extract_gear_positions(schematic)
    solution = 0
    for (x, y) in gear_positions:
        surrounding_numbers = []
        for line in range(max(0, y - 1), min(len(schematic), y + 2)):
            for number in numbers_by_line[line]:
                if number.does_symbol_touch(x, y):
                    surrounding_numbers.append(number)
        if len(surrounding_numbers) == 2:
            solution += surrounding_numbers[0].value * \
                surrounding_numbers[1].value
    print(solution)


if __name__ == '__main__':
    solve_part2('input')
