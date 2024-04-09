import numpy as np
import os.path
import json
import re
from parse import parse_file

DIRS = [np.array((1, 0)), np.array((0, 1)),
        np.array((-1, 0)), np.array((0, -1))]
BUCKETS = [np.array((0, 0)), np.array((1, 0)), np.array((1, 1)),
           np.array((0, 1)), np.array((-1, 1)), np.array((-1, 0)),
           np.array((-1, -1)), np.array((0, -1)), np.array((1, -1))]


def solve_part1(filename):
    garden = np.array(parse_file(filename, list))
    np.pad(garden, 1, constant_values='#')
    (y,), (x,) = np.where(garden == 'S')
    garden[y, x] = '.'
    reachable_mask = np.zeros_like(garden, dtype=int)
    reachable_mask[y, x] = 1
    for _ in range(64):
        reachable_mask = advance_one_step(garden, reachable_mask)
    print(np.count_nonzero(reachable_mask))


def advance_one_step(garden, reachable_mask):
    result = np.zeros_like(garden, dtype=int)
    ys, xs = np.where(reachable_mask == 1)
    for y, x in zip(ys, xs):
        for dy, dx in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if garden[y + dy, x + dx] == '.':
                result[y + dy, x + dx] = 1
    return result


def solve_part2(filename, steps):
    garden = np.array(parse_file(filename, list))
    (y,), (x,) = np.where(garden == 'S')
    garden[y, x] = '.'
    if os.path.exists(f'{filename}_log_by_bucket.json'):
        with open(f'{filename}_log_by_bucket.json', 'r') as file:
            encoding = json.load(file)
        decoded_keys = []
        for key in encoding.keys():
            integer_strings = re.findall('[-+]?[0-9]+', key)
            decoded_keys.append(tuple(map(int, integer_strings)))
        log_by_bucket = {decoded_key: encoding[str(
            decoded_key)] for decoded_key in decoded_keys}
    else:
        log_by_bucket = {}
        print(garden.shape)
        for bucket in BUCKETS:
            y_start, x_start = (-bucket[0]) * y + y, (-bucket[1]) * x + x
            print(bucket, x_start, y_start)
            log_by_bucket[tuple(bucket)] = compute_reachable_log(
                garden, x_start, y_start)
        encoding = {str(bucket): log for (bucket, log)
                    in log_by_bucket.items()}
        encoding = json.dumps(encoding, indent=4)
        with open(f'{filename}_log_by_bucket.json', 'w') as file:
            file.write(encoding)
    print({bucket: len(log) for (bucket, log) in log_by_bucket.items()})
    inner_area = compute_inner_area(log_by_bucket, garden.shape[0], steps)
    print(inner_area)
    perimeter_area = compute_perimeter_area(
        log_by_bucket, garden.shape[0], steps)
    print(perimeter_area)
    print(inner_area + perimeter_area)
    upper_bound = compute_inner_area(
        log_by_bucket, garden.shape[0], steps + 262)
    print(
        f'Upper Bound: {upper_bound}')
    print(f'difference: {upper_bound - inner_area - perimeter_area}')


def array_to_string(arr):
    return '\n'.join((''.join(map(str, row)) for row in arr))


def compute_fill_time(padded_garden, x_start, y_start):
    covered_cells = np.where(padded_garden == '#', 1, 0)
    covered_cells[y_start, x_start] = 1
    fill_time = 0
    point_queue = [np.array((y_start, x_start))]
    while point_queue:
        next_queue = []
        for current_point in point_queue:
            for dir in DIRS:
                if covered_cells[tuple(current_point + dir)] == 0:
                    next_queue.append(current_point + dir)
                covered_cells[tuple(current_point + dir)] = 1
        point_queue = next_queue
        fill_time += 1
    return fill_time


def compute_reachable_log(garden, x_start, y_start):
    padded_garden = np.pad(garden, 1, constant_values='#')
    log = [np.zeros_like(padded_garden, dtype=int)]
    log[0][y_start + 1, x_start + 1] = 1
    log.append(advance_one_step(padded_garden, log[-1]))
    while True:
        next_mask = advance_one_step(padded_garden, log[-1])
        if np.array_equal(next_mask, log[-2]):
            return list(map(lambda a: np.count_nonzero(a), log))
        log.append(next_mask)


def norm_1(arr):
    return np.sum(np.abs(np.array(arr)))


def compute_steps_to_reach_garden(garden_length, plot_x, plot_y):
    start_pos = (garden_length - 1) // 2
    return garden_length * norm_1((plot_x, plot_y)) - start_pos * norm_1(np.sign((plot_x, plot_y)))


def compute_steps_to_fill_garden(log_by_bucket, garden_length, plot_x, plot_y):
    bucket = tuple(np.sign((plot_y, plot_x)))
    return compute_steps_to_reach_garden(garden_length, plot_x, plot_y) + len(log_by_bucket[bucket])


def compute_inner_area(log_by_bucket, length, steps):
    green_plot_count = 0
    red_plot_count = 0
    if steps >= len(log_by_bucket[(0, 0)]):
        green_plot_count += 1
    if steps > len(log_by_bucket[(1, 0)]) + (length - 1) // 2:
        axis_plot_steps = (
            steps - length) // length
        print(axis_plot_steps)
        print(compute_steps_to_fill_garden(
            log_by_bucket, length, axis_plot_steps, 0))
        green_plot_count += 4 * (axis_plot_steps // 2 + axis_plot_steps % 2)
        red_plot_count += 4 * (axis_plot_steps // 2)
        print(green_plot_count, red_plot_count)
    if steps > len(log_by_bucket[(1, 1)]) + length:
        corner_plot_steps = (
            steps - length) // length
        print(corner_plot_steps)
        print(compute_steps_to_fill_garden(
            log_by_bucket, length, corner_plot_steps - 1, 1))
        green_plot_count += 4 * (corner_plot_steps //
                                 2 + corner_plot_steps % 2)**2

        def consecutive_sum(n): return (n * (n + 1)) // 2
        red_plot_count += 8 * consecutive_sum(corner_plot_steps // 2)
        print(green_plot_count, red_plot_count)
    center_plot_modality = (steps - len(log_by_bucket[(0, 0)])) % 2
    green_plot_area = log_by_bucket[(0, 0)][-(center_plot_modality + 1)]
    red_plot_area = log_by_bucket[(0, 0)][-((1 - center_plot_modality) + 1)]
    print(green_plot_area, red_plot_area)
    return green_plot_count * green_plot_area + red_plot_count * red_plot_area


def compute_perimeter_area(log_by_bucket, length, steps):
    if steps < (length + 1) // 2:
        return log_by_bucket[(0, 0)][steps]
    if steps < length:
        return log_by_bucket[(0, 0)][steps] \
            + sum((log_by_bucket[tuple(bucket)][steps -
                  (length + 1) // 2] for bucket in DIRS))
    fill_steps = (steps - length) // length
    axis_steps = (steps + (length - 1) // 2) // length
    corner_steps = (steps + length - 1) // length
    print(fill_steps, axis_steps, corner_steps)
    perimeter_area = 0
    for garden_steps in range(fill_steps + 1, axis_steps + 1):
        remaining_steps = steps - \
            compute_steps_to_reach_garden(length, garden_steps, 0)
        print(remaining_steps)
        for bucket in DIRS:
            perimeter_area += log_by_bucket[tuple(bucket)][remaining_steps]
    for garden_steps in range(fill_steps + 1, corner_steps + 1):
        remaining_steps = steps - \
            compute_steps_to_reach_garden(length, garden_steps - 1, 1)
        print(remaining_steps)
        for bucket in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            perimeter_area += log_by_bucket[bucket][remaining_steps]
    return perimeter_area


if __name__ == '__main__':
    solve_part1('input')
    solve_part2('input', 26501365)
