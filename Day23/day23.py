from parse import parse_file
import numpy as np

DIRS = [np.array([1, 0]), np.array([0, 1]),
        np.array([-1, 0]), np.array([0, -1])]
ARROW_TO_DIR = {'v': DIRS[0], '>': DIRS[1], '^': DIRS[2], '<': DIRS[3]}


def solve_part1(filename):
    maze = np.asarray(parse_file(filename, list))
    maze = np.pad(maze, 1, constant_values='#')
    start_y = 1
    ((start_x,),) = np.where(maze[1] == '.')
    end_y = maze.shape[0] - 2
    ((end_x,),) = np.where(maze[-2] == '.')

    (vertices, edges, costs) = compute_intersection_connection_graph(
        maze, (start_y, start_x), (end_y, end_x))
    dists = compute_longest_distances(
        vertices, edges, costs, (start_y, start_x))
    print(dists[(end_y, end_x)])


def print_maze(maze):
    print('\n'.join((''.join(row) for row in maze)))


def print_height_map(height_map):
    print('\n'.join((''.join(map(lambda c: ' ' if c == 0 else str(c), row))
          for row in height_map)))


def compute_height_map(maze, start_point):
    height_map = np.zeros_like(maze, dtype=int)
    point_queue = [(np.asarray(start_point), -1)]
    while point_queue:
        (current_point, current_height) = point_queue.pop(0)
        if maze[tuple(current_point)] == '#' or (height_map[tuple(current_point)] != 0 and height_map[tuple(current_point)] >= current_height):
            continue
        height_map[tuple(current_point)] = current_height
        if maze[tuple(current_point)] == '.':
            for direction in DIRS:
                point_queue.append((current_point + direction, current_height))
        else:
            point_queue.append(
                (current_point + ARROW_TO_DIR[maze[tuple(current_point)]], current_height - 1))
    max_height = -np.min(height_map)
    return np.where(height_map != 0, height_map + max_height + 1, 0)


def print_height_map_embedded_in_maze(maze, height_map):
    def cell_to_string(y, x):
        if maze[y, x] != '.':
            return maze[y, x]
        else:
            return str(height_map[y, x])

    def row_to_string(y):
        return ''.join(cell_to_string(y, x) for x in range(maze.shape[1]))

    print('\n'.join(row_to_string(y) for y in range(maze.shape[0])))


def find_intersections(maze):
    intersections = []
    for point in zip(*np.where(maze == '.')):
        # print(f'current_point: {point}')
        point = np.asarray(point)
        possible_direction_count = 0
        for direction in DIRS:
            if maze[tuple(point + direction)] != '#':
                # print(
                #     f'In direction {direction} found {maze[tuple(point + direction)]}')
                possible_direction_count += 1
        if possible_direction_count > 2:
            intersections.append(tuple(point))
    return intersections


def compute_intersection_connection_graph(maze, start_point, end_point):
    intersections = find_intersections(maze)
    edges = {intersection: [] for intersection in intersections}
    edges[start_point] = []
    edges[end_point] = []
    costs = {}
    (intersection_connected_to_start, steps_taken) = follow_path_until_intersection(
        maze, start_point, DIRS[0])
    edges[start_point].append(intersection_connected_to_start)
    costs[(start_point, intersection_connected_to_start)] = steps_taken
    for intersection in intersections:
        intersec_arr = np.asarray(intersection)
        for direction in DIRS:
            if maze[tuple(intersec_arr + direction)] == '#':
                continue
            arrow_direction = ARROW_TO_DIR[maze[tuple(
                intersec_arr + direction)]]
            if np.array_equal(direction, -arrow_direction):
                continue
            (connected_intersection, steps_taken) = follow_path_until_intersection(
                maze, intersec_arr + 2 * direction, direction)
            edges[intersection].append(connected_intersection)
            costs[(intersection, connected_intersection)] = steps_taken + 2
    intersections.append(start_point)
    intersections.append(end_point)
    return (intersections, edges, costs)


def follow_path_until_intersection(maze, start_point, start_direction):
    steps_taken = 0
    current_point = np.asarray(start_point)
    current_direction = np.asarray(start_direction)
    zero_point = np.asarray([0, 0])
    while maze[tuple(current_point)] == '.':
        has_moved = False
        for direction in DIRS:
            if np.array_equal(current_direction + direction, zero_point):
                continue
            if maze[tuple(current_point + direction)] != '#':
                current_direction = direction
                current_point = current_point + direction
                has_moved = True
                break
        if not has_moved:
            return (tuple(current_point), steps_taken)
        steps_taken += 1
    current_point += ARROW_TO_DIR[maze[tuple(current_point)]]
    steps_taken += 1
    return (tuple(current_point), steps_taken)


def compute_longest_distances(vertices, edges, costs, start_vertex):
    dists = {start_vertex: 0}

    def compute_longest_distance_to_vertex(vertex):
        if dists.get(vertex) is not None:
            return dists[vertex]

        current_dist = 0
        for vert in vertices:
            if vertex in edges[vert]:
                compare_dist = compute_longest_distance_to_vertex(
                    vert) + costs[(vert, vertex)]
                if current_dist < compare_dist:
                    current_dist = compare_dist
        dists[vertex] = current_dist
        return current_dist
    for vertex in vertices:
        compute_longest_distance_to_vertex(vertex)
    return dists


if __name__ == '__main__':
    solve_part1('input')
