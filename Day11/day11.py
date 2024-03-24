from parse import parse_file
import numpy as np


def solve_part1(filename):
    galaxy = np.array(parse_file(filename, parse_line=list))
    expanded_galaxy = expand_galaxy(galaxy)
    star_positions = np.argwhere(np.where(expanded_galaxy == '#', 1, 0))
    solution = 0
    for i in range(len(star_positions)):
        for j in range(i+1, len(star_positions)):
            solution += np.sum(np.abs(star_positions[j] - star_positions[i]))
    print(solution)


def expand_galaxy(galaxy):
    space = np.where(galaxy == '.', 1, 0)
    (free_rows,) = np.nonzero(np.all(space, axis=1))
    (free_cols,) = np.nonzero(np.all(space, axis=0))
    expanded_galaxy = np.full(
        (space.shape[0] + len(free_rows), space.shape[1] + len(free_cols)), '.')
    for (y, x) in np.argwhere(np.where(galaxy == '#', 1, 0)):
        y_offset = np.count_nonzero(np.where(free_rows < y, 1, 0))
        x_offset = np.count_nonzero(np.where(free_cols < x, 1, 0))
        expanded_galaxy[y + y_offset, x + x_offset] = '#'
    return expanded_galaxy


def print_galaxy(galaxy):
    for row in galaxy:
        print(''.join(row))


def compute_lambda(x_0, y_0, x_1, y_1, free_rows_cumsum, free_cols_cumsum):
    lambda_x = np.abs(free_cols_cumsum[x_1] - free_cols_cumsum[x_0])
    lambda_y = np.abs(free_rows_cumsum[y_1] - free_rows_cumsum[y_0])
    return lambda_x + lambda_y


def solve_part2(filename, expansion_constant=int(1e6)):
    galaxy = np.array(parse_file(filename, parse_line=list))
    space = np.where(galaxy == '.', 1, 0)
    free_rows_cumsum = np.cumsum(np.all(space, axis=1))
    free_cols_cumsum = np.cumsum(np.all(space, axis=0))
    star_positions = np.argwhere(np.where(galaxy == '#', 1, 0))
    solution = 0
    for (i, (y, x)) in enumerate(star_positions):
        for (y_, x_) in star_positions[i+1:]:
            lambda_ = compute_lambda(
                x, y, x_, y_, free_rows_cumsum, free_cols_cumsum)
            delta = np.abs(x - x_) + np.abs(y - y_)
            solution += delta + (expansion_constant - 1) * lambda_
    print(solution)


if __name__ == '__main__':
    solve_part1('input')
    solve_part2('input', 2)
    solve_part2('example', 2)
    solve_part2('example', 10)
    solve_part2('example', 100)
    solve_part2('input')
