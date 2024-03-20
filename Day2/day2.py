import re


def parse_file(filename, parse_line):
    with open(filename, 'r') as file:
        lines = file.readlines()
        lines = list(map(lambda line: line.split('\n')[0], lines))
        if lines[-1] == '':
            lines.pop()

    parsed_file = list(map(parse_line, lines))
    return parsed_file


def parse_line(line):
    game_id = int(re.search('^Game ([0-9]+): ', line).group(1))
    game = line.split(': ')[1]
    rounds = game.split('; ')
    parsed_rounds = []
    for round in rounds:
        parsed_round = [0, 0, 0]    # r g b counts
        round = round.split(', ')
        for substring in round:
            (count, color) = re.search(
                '([0-9]+) (red|green|blue)', substring).groups()
            count = int(count)
            if color == 'red':
                parsed_round[0] = count
            elif color == 'green':
                parsed_round[1] = count
            else:
                parsed_round[2] = count
        parsed_rounds.append(parsed_round)
    return (game_id, parsed_rounds)


def is_game_possible(game, true_cube_counts):
    for round in game:
        for (current_count, true_count) in zip(round, true_cube_counts):
            if current_count > true_count:
                return False
    return True


def solve_part1(filename):
    parsed = parse_file(filename, parse_line)
    solution = 0
    for (id, game) in parsed:
        if is_game_possible(game, [12, 13, 14]):
            solution += id
    print(f'The sum of IDs of possible games is: {solution}')


def compute_power_of_game(game):
    least_necessary_cube_counts = [0, 0, 0]
    for round in game:
        for (i, cube_count) in enumerate(round):
            if cube_count > least_necessary_cube_counts[i]:
                least_necessary_cube_counts[i] = cube_count

    return least_necessary_cube_counts[0] * least_necessary_cube_counts[1] * least_necessary_cube_counts[2]


def solve_part2(filename):
    parsed = parse_file(filename, parse_line)
    solution = 0
    for (_, game) in parsed:
        solution += compute_power_of_game(game)
    print(f'The sum of the powers of all games is: {solution}')


if __name__ == '__main__':
    solve_part2('input')
