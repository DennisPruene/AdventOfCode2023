from parse import parse_file
import numpy as np


def solve_part1(filename):
    picture = np.array(parse_file(filename, parse_line=list))
    slide_north(picture)
    print('\n'.join(''.join(row) for row in picture))
    print(compute_load(picture))


def solve_part2(filename, target_steps=1000000000):
    picture = np.array(parse_file(filename, parse_line=list))
    sequence = [picture.copy()]
    do_cycle(picture)
    while all(not np.array_equal(recorded_picture, picture) for recorded_picture in sequence):
        sequence.append(picture.copy())
        do_cycle(picture)
    period_start = None
    for i in range(len(sequence)):
        if np.array_equal(sequence[i], picture):
            period_start = i
            break
    period = len(sequence) - period_start
    target_steps -= period_start
    print(sequence[period_start + (target_steps % period)])
    print(compute_load(sequence[period_start + (target_steps % period)]))


def slide_north(picture):
    for col in picture.T:
        next_empty_position = 0
        for i in range(len(col)):
            if col[i] == 'O':
                col[i] = '.'
                col[next_empty_position] = 'O'
                next_empty_position += 1
            elif col[i] == '#':
                next_empty_position = i + 1


def slide(picture, x_dir, y_dir):
    if x_dir == 0 and y_dir == -1:
        slide_north(picture)
    elif x_dir == 0 and y_dir == 1:
        slide_north(picture[::-1])
    elif x_dir == -1 and y_dir == 0:
        slide_north(picture.T)
    else:
        slide_north(picture.T[::-1])


def do_cycle(picture):
    for (x_dir, y_dir) in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
        slide(picture, x_dir, y_dir)


def compute_load(picture):
    load = 0
    for (i, row) in enumerate(picture[::-1]):
        load_factor = i + 1
        load += np.count_nonzero(np.where(row == 'O', 1, 0)) * load_factor
    return load


if __name__ == '__main__':
    solve_part1('input')
    solve_part2('input')
