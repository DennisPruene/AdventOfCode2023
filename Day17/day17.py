from parse import parse_file
from priority_queue import PriorityQueue
from heat_map import HeatMap
import numpy as np

LEFT_TURN_MATRIX = np.array([[0, -1],
                             [1, 0]])
RIGHT_TURN_MATRIX = np.array([[0, 1],
                              [-1, 0]])
DIRECTIONS = [np.array((1, 0)), np.array(
    (0, 1)), np.array((-1, 0)), np.array((0, -1))]
DIR_INDICES = {(1, 0): 0, (0, 1): 1, (-1, 0): 2, (0, -1): 3}
DIRECTION_CHARS = ['v', '>', '^', '<']


def parse_line(line):
    return [int(char) for char in line]


def solve_part1(filename, min_step, max_step):
    heat_map = HeatMap(
        np.array(parse_file(filename, parse_line=parse_line)), min_step, max_step)
    (distances, _, min_heat_loss) = heat_map.dijkstra()
    print(min_heat_loss[-1, -1])


def paint_path(picture, distances, previous_nodes, dest):
    path = picture.astype(str)
    last_position = dest
    minimal_direction = None
    minimal_steps_left = None
    minimal_distance = 2**31
    for direction in DIRECTIONS:
        for steps_left in range(3):
            if (last_position, tuple(direction), steps_left) in distances and distances[(last_position, tuple(direction), steps_left)] < minimal_distance:
                minimal_distance = distances[(
                    last_position, tuple(direction), steps_left)]
                minimal_steps_left = steps_left
                minimal_direction = tuple(direction)
    print(minimal_distance)
    while any(last_position):
        dir_index = DIR_INDICES[minimal_direction]
        path[last_position] = DIRECTION_CHARS[dir_index]
        (last_position, minimal_direction, minimal_steps_left) = previous_nodes[(
            last_position, minimal_direction, minimal_steps_left)]
    return path


def is_position_in_bounds(picture, position):
    return position[0] >= 0 and position[1] >= 0 and position[0] < picture.shape[0] \
        and position[1] < picture.shape[1]


def dijkstra(picture, source=np.array([0, 0])):
    distances = {(tuple(source), tuple(direction), 3)
                  : 0 for direction in DIRECTIONS}
    previous_nodes = {}
    queue = PriorityQueue()
    for source_node in distances.keys():
        queue.add_with_priority(source_node, 0)

    while queue:
        (position, direction, steps_left) = queue.extract_min()
        print(position, direction, steps_left)
        position = np.array(position)
        direction = np.array(direction)
        current_distance = distances[(
            tuple(position), tuple(direction), steps_left)]
        left_turn = LEFT_TURN_MATRIX.dot(direction)
        right_turn = RIGHT_TURN_MATRIX.dot(direction)
        next_nodes = [(position + direction, direction, steps_left - 1),
                      (position + left_turn, left_turn, 2),
                      (position + right_turn, right_turn, 2)]
        for (next_position, next_direction, next_steps_left) in next_nodes:
            if next_steps_left < 0 or not is_position_in_bounds(picture, next_position):
                continue
            key_of_node = (tuple(next_position), tuple(
                next_direction), next_steps_left)
            next_distance = current_distance + \
                int(picture[tuple(next_position)])
            if key_of_node not in distances:
                queue.add_with_priority(
                    key_of_node, next_distance)
                distances[key_of_node] = next_distance
                previous_nodes[key_of_node] = (
                    tuple(position), tuple(direction), steps_left)
            elif distances[key_of_node] > next_distance:
                queue.decrease_priority(
                    key_of_node, next_distance)
                distances[key_of_node] = next_distance
                previous_nodes[key_of_node] = (
                    tuple(position), tuple(direction), steps_left)
    return (distances, previous_nodes)


if __name__ == '__main__':
    solve_part1('input', 1, 3)
    solve_part1('example', 4, 10)
    solve_part1('input', 4, 10)
