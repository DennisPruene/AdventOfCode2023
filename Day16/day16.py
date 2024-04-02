from parse import parse_file
from functools import reduce
import numpy as np

DIRECTION_CONVERSION_MATRICES = {
    '.': [np.array([[1, 0],
                    [0, 1]])],
    '/': [np.array([[0, -1],
                    [-1, 0]])],
    '\\': [np.array([[0, 1],
                     [1, 0]])],
    '-': [np.array([[0, 0],
                    [1, 1]]),
          np.array([[0, 0],
                    [-1, 1]])],
    '|': [np.array([[1, 1],
                    [0, 0]]),
          np.array([[1, -1],
                    [0, 0]])],
}


def solve_part1(filename):
    picture = np.array(parse_file(filename, parse_line=list))
    print(propagate_light(picture, np.array([0, 0]), np.array([0, 1])))


def solve_part2(filename):
    picture = np.array(parse_file(filename, parse_line=list))
    max_energized_tiles = 0
    for i in range(picture.shape[0]):
        max_energized_tiles = max(max_energized_tiles, propagate_light(
            picture, np.array([i, 0]), np.array([0, 1])))
        max_energized_tiles = max(max_energized_tiles, propagate_light(
            picture, np.array([i, -1]), np.array([0, -1])))
    for i in range(picture.shape[1]):
        max_energized_tiles = max(max_energized_tiles, propagate_light(
            picture, np.array([0, i]), np.array([1, 0])))
        max_energized_tiles = max(max_energized_tiles, propagate_light(
            picture, np.array([-1, i]), np.array([-1, 0])))
    print(max_energized_tiles)


def propagate_light(picture, initial_position, initial_direction):
    beam_masks = {
        direction: np.zeros_like(picture, dtype=int) for direction in [(1, 0), (0, 1), (-1, 0), (0, -1)]
    }
    beam_queue = [(initial_position, initial_direction)]
    while len(beam_queue):
        (position, direction) = beam_queue.pop(0)
        if position[0] < 0 or position[1] < 0 or position[0] >= picture.shape[0] or position[1] >= picture.shape[1] or beam_masks[tuple(direction)][tuple(position)]:
            continue

        beam_masks[tuple(direction)][tuple(position)] = 1
        for conversion_matrix in DIRECTION_CONVERSION_MATRICES[picture[tuple(position)]]:
            next_direction = conversion_matrix.dot(direction)
            next_position = position + next_direction
            beam_queue.append((next_position, next_direction))
    energized_tiles = reduce(
        np.logical_or, beam_masks.values(), np.zeros_like(picture, dtype=int))
    return np.count_nonzero(energized_tiles)


if __name__ == '__main__':
    solve_part1('input')
    solve_part2('input')
