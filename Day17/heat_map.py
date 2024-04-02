import numpy as np
from priority_queue import PriorityQueue
import heapq

LEFT_TURN_MATRIX = np.array([[0, -1],
                             [1, 0]])
RIGHT_TURN_MATRIX = np.array([[0, 1],
                              [-1, 0]])
DIRECTIONS = [np.array((1, 0)), np.array(
    (0, 1)), np.array((-1, 0)), np.array((0, -1))]
DIR_INDICES = {(1, 0): 0, (0, 1): 1, (-1, 0): 2, (0, -1): 3}


class HeatMap:
    def __init__(self, heat_map, min_step=1, max_step=3):
        self.heat_map = heat_map
        self.min_step = min_step
        self.max_step = max_step
        self.node_count = heat_map.shape[0] * \
            heat_map.shape[1] * 4 * max_step + 1
        self.data_to_node = np.arange(1, self.node_count).reshape(
            (4, max_step, heat_map.shape[0], heat_map.shape[1]))
        self.node_to_data = [None]
        for i in range(4):
            for j in range(max_step):
                for k in range(heat_map.shape[0]):
                    for l in range(heat_map.shape[1]):
                        # print(self.data_to_node[i, j, k, l])
                        self.node_to_data.append((i, j, k, l))

    def get_heat_loss(self, position):
        return self.heat_map[tuple(position)]

    def get_node_position(self, node):
        if node == 0:
            return np.array((0, 0))
        (_, _, y, x) = self.node_to_data[node]
        return np.array((y, x))

    def get_node_direction(self, node):
        if node == 0:
            raise IndexError
        (dir_index, _, _, _) = self.node_to_data[node]
        return DIRECTIONS[dir_index]

    def get_node_steps_left(self, node):
        if node == 0:
            return 3
        (_, result, _, _) = self.node_to_data[node]
        return result

    def get_node(self, position, direction, steps_left):
        return self.data_to_node[DIR_INDICES[tuple(direction)], steps_left, position[0], position[1]]

    def is_position_in_bounds(self, position):
        return position[0] >= 0 and position[1] >= 0 and position[0] < self.heat_map.shape[0] and position[1] < self.heat_map.shape[1]

    def get_edges(self, node):
        if node == 0:
            down_node = self.get_node([1, 0], [1, 0], self.max_step - 1)
            right_node = self.get_node([0, 1], [0, 1], self.max_step - 1)
            return [down_node, right_node]

        result = []
        position = self.get_node_position(node)
        direction = self.get_node_direction(node)
        steps_left = self.get_node_steps_left(node)
        left_direction = LEFT_TURN_MATRIX.dot(direction)
        right_direction = RIGHT_TURN_MATRIX.dot(direction)
        left_position = position + left_direction
        straight_position = position + direction
        right_position = position + right_direction
        if steps_left <= self.max_step - self.min_step and self.is_position_in_bounds(left_position):
            left_node = self.get_node(
                left_position, left_direction, self.max_step - 1)
            result.append(left_node)
        if steps_left and self.is_position_in_bounds(straight_position):
            straight_node = self.get_node(
                straight_position, direction, steps_left - 1)
            result.append(straight_node)
        if steps_left <= self.max_step - self.min_step and self.is_position_in_bounds(right_position):
            right_node = self.get_node(
                right_position, right_direction, self.max_step - 1)
            result.append(right_node)
        return result

    def get_cost(self, from_node, to_node):
        from_position = self.get_node_position(from_node)
        to_position = self.get_node_position(to_node)
        if tuple(to_position - from_position) in DIR_INDICES:
            return self.get_heat_loss(to_position)
        else:
            print(
                f"Warning: {from_position} and {to_position} are too far apart!")
            return float('inf')

    def dijkstra(self, source=0):
        distances = np.array([float('inf') for _ in range(self.node_count)])
        prev_nodes = [None for _ in range(self.node_count)]
        distances[source] = 0
        queue = [(0, source)]
        while queue:
            (current_distance, current_node) = heapq.heappop(queue)
            for next_node in self.get_edges(current_node):
                next_distance = current_distance + \
                    self.get_cost(current_node, next_node)
                if next_distance < distances[next_node]:
                    heapq.heappush(queue, (next_distance, next_node))
                    distances[next_node] = next_distance
                    prev_nodes[next_node] = current_node

        min_heat_loss = np.min(distances[1:].reshape(
            (4, self.max_step, self.heat_map.shape[0], self.heat_map.shape[1])), axis=(0, 1))
        min_heat_loss[0, 0] = 0
        return (distances, prev_nodes, min_heat_loss)


if __name__ == '__main__':
    from parse import parse_file

    def parse_line(line):
        return [int(char) for char in line]

    heat_map = HeatMap(np.array(parse_file('small_example', parse_line)), 3)
    for node in range(1, heat_map.node_count):
        compare_to = heat_map.data_to_node[heat_map.node_to_data[node]]
        print(node, compare_to)
