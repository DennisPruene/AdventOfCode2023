from parse import parse_file
import re


def parse_line(line):
    card_id = int(re.search('^Card +([0-9]+)', line).group(1))
    line = re.split(': *', line)[1]
    (winning_numbers, numbers_you_have) = re.split('\| *', line)
    winning_numbers = re.split(' *$', winning_numbers)[0]
    numbers_you_have = re.split(' *$', numbers_you_have)[0]
    winning_numbers = list(map(int, re.split(' +', winning_numbers)))
    numbers_you_have = list(map(int, re.split(' +', numbers_you_have)))
    return (card_id, winning_numbers, numbers_you_have)


def compute_card_points(winning_numbers, numbers_you_have):
    points = 0
    for number in numbers_you_have:
        if number in winning_numbers:
            if points == 0:
                points = 1
            else:
                points *= 2
    return points


def compute_match_number(winning_numbers, numbers_you_have):
    matches = 0
    for number in numbers_you_have:
        if number in winning_numbers:
            matches += 1
    return matches


def solve_part1(filename):
    cards = parse_file(filename, parse_line)
    solution = 0
    for (_, winning_numbers, numbers_you_have) in cards:
        solution += compute_card_points(winning_numbers, numbers_you_have)
    print(solution)


def solve_part2(filename):
    cards = parse_file(filename, parse_line)
    card_counts = {card_id: 1 for (card_id, _, _) in cards}
    for current_card_id in range(1, len(cards)+1):
        match_number = compute_match_number(
            cards[current_card_id-1][1], cards[current_card_id-1][2])
        for i in range(1, match_number+1):
            card_counts[current_card_id + i] += card_counts[current_card_id]
    solution = sum(card_counts.values())
    print(solution)


if __name__ == '__main__':
    solve_part2('input')
