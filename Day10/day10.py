from parse import parse_file
import sys

sys.setrecursionlimit(10000)

VERTICAL_PIPE = '|'
HORIZONTAL_PIPE = '-'
DOWNRIGHT_PIPE = 'F'
DOWNLEFT_PIPE = '7'
UPRIGHT_PIPE = 'L'
UPLEFT_PIPE = 'J'
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
DIRECTIONS_TO_PIPE = {frozenset(((1, 0), (0, 1))): 'F',
                      frozenset(((1, 0), (-1, 0))): '-',
                      frozenset(((1, 0), (0, -1))): 'L',
                      frozenset(((0, 1), (-1, 0))): '7',
                      frozenset(((0, 1), (0, -1))): '|',
                      frozenset(((-1, 0), (0, -1))): 'J'}
PIPE_TO_DIRECTIONS = {pipe: dirs for (
    dirs, pipe) in DIRECTIONS_TO_PIPE.items()}
PIPE_TO_DIRECTIONS['.'] = frozenset()


def scan_for_starting_position(pipe_grid):
    for (y, row) in enumerate(pipe_grid):
        if 'S' in row:
            return (row.index('S'), y)


def pad_grid(pipe_grid):
    for row in pipe_grid:
        row = '.' + row + '.'
    pipe_grid.insert(0, '.' * len(pipe_grid[0]))
    pipe_grid.append('.' * len(pipe_grid[0]))


def iter_neighbors(x, y):
    return iter([(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)])


def reverse_direction(direction):
    return tuple((-axis for axis in direction))


def solve_part1(filename):
    pipe_grid = parse_file(filename)
    pad_grid(pipe_grid)
    for row in pipe_grid:
        print(row)
    (x_s, y_s) = scan_for_starting_position(pipe_grid)
    connected_starting_directions = []
    for dir in DIRECTIONS:
        if reverse_direction(dir) in PIPE_TO_DIRECTIONS[pipe_grid[y_s + dir[1]][x_s + dir[0]]]:
            connected_starting_directions.append(dir)
    pipe_grid[y_s] = pipe_grid[y_s][:x_s] + DIRECTIONS_TO_PIPE[frozenset(
        connected_starting_directions)] + pipe_grid[y_s][x_s+1:]
    print(pipe_grid[y_s][x_s])
    distances = [[len(pipe_grid) * len(pipe_grid[0]) for _ in range(len(pipe_grid[0]))]
                 for _ in range(len(pipe_grid))]
    distances[y_s][x_s] = 0
    print(distances)
    for starting_direction in connected_starting_directions:
        current_position = (x_s, y_s)
        current_distance = 0
        current_direction = starting_direction
        next_position = (
            current_position[0] + current_direction[0], current_position[1] + current_direction[1])
        while distances[next_position[1]][next_position[0]] > current_distance + 1:
            current_distance += 1
            current_position = next_position
            distances[current_position[1]
                      ][current_position[0]] = current_distance
            current_direction = PIPE_TO_DIRECTIONS[pipe_grid[current_position[1]][current_position[0]]].difference(
                (reverse_direction(current_direction),)).__iter__().__next__()
            next_position = (
                current_position[0] + current_direction[0], current_position[1] + current_direction[1])

    for y in range(len(distances)):
        for x in range(len(distances[0])):
            if distances[y][x] == len(pipe_grid) * len(pipe_grid[0]):
                distances[y][x] = -1

    print(max((max(row) for row in distances)))


def replace_starting_tile_with_pipe(pipe_grid, x_s, y_s):
    starting_tile_directions = []
    for (x_d, y_d) in DIRECTIONS:
        if (-x_d, -y_d) in PIPE_TO_DIRECTIONS[pipe_grid[y_s + y_d][x_s + x_d]]:
            starting_tile_directions.append((x_d, y_d))
    pipe_grid[y_s] = pipe_grid[y_s][:x_s] + DIRECTIONS_TO_PIPE[frozenset(
        starting_tile_directions)] + pipe_grid[y_s][x_s + 1:]


def compute_loop_path(pipe_grid, x_s, y_s):
    loop_path = [(x_s, y_s)]
    (x_d, y_d) = next(iter(PIPE_TO_DIRECTIONS[pipe_grid[y_s][x_s]]))
    while (x_s + x_d, y_s + y_d) != loop_path[0]:
        (x_s, y_s) = (x_s + x_d, y_s + y_d)
        (x_d, y_d) = next(iter(PIPE_TO_DIRECTIONS[pipe_grid[y_s][x_s]].difference(
            (reverse_direction((x_d, y_d)),))))
        loop_path.append((x_s, y_s))
    return loop_path


def enlarge_pipe_grid(pipe_grid, loop_path):
    enlarged_pipe_grid = [list('.' * (2 * len(pipe_grid[0])))
                          for _ in range(2 * len(pipe_grid))]
    for ((x_curr, y_curr), (x_next, y_next)) in zip(loop_path, loop_path[1:] + [loop_path[0]]):
        (x_dir, y_dir) = (x_next - x_curr, y_next - y_curr)
        enlarged_pipe_grid[2 * y_curr][2 * x_curr] = pipe_grid[y_curr][x_curr]
        bridge_pipe = None
        if x_dir != 0:
            bridge_pipe = '-'
        else:
            bridge_pipe = '|'
        enlarged_pipe_grid[2 * y_curr +
                           y_dir][2 * x_curr + x_dir] = bridge_pipe
    return enlarged_pipe_grid


def spread_oxygen(pipe_grid, x, y):
    point_queue = [(x, y)]
    while len(point_queue):
        (x, y) = point_queue.pop(0)
        if pipe_grid[y][x] != '.':
            continue

        pipe_grid[y][x] = 'O'
        for (x_d, y_d) in DIRECTIONS:
            point_queue.append((x + x_d, y + y_d))


def solve_part2(filename):
    pipe_grid = parse_file(filename)
    pad_grid(pipe_grid)
    (x_s, y_s) = scan_for_starting_position(pipe_grid)
    replace_starting_tile_with_pipe(pipe_grid, x_s, y_s)
    loop_path = compute_loop_path(pipe_grid, x_s, y_s)
    enlarged_pipe_grid = enlarge_pipe_grid(pipe_grid, loop_path)
    spread_oxygen(enlarged_pipe_grid, 0, 0)
    enclosed_tiles = [[1 if tile == '.' else 0 for tile in row[::2]]
                      for row in enlarged_pipe_grid[::2]]
    print(sum((sum(row) for row in enclosed_tiles)))


if __name__ == '__main__':
    solve_part1('input')
    solve_part2('input')
