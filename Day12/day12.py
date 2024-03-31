from parse import parse_file, extract_integers
from itertools import combinations
import numpy as np


def parse_line(line):
    (known_state, redundancy) = line.split(' ')
    redundancy = tuple(extract_integers(redundancy))
    return (known_state, redundancy)


def solve_part1(filename, repeat=1):
    tool_chart = parse_file(filename, parse_line)
    print(tool_chart)
    solution = 0
    for (i, (known_state, redundancy)) in enumerate(tool_chart):
        print(f'{i/len(tool_chart)*100}% complete!')
        known_state = '?'.join([known_state] * repeat)
        cur_count = compute_possibility_count_dp(
            known_state, redundancy * repeat)
        solution += cur_count

    print(solution)


def is_state_possible(state, redundancy):
    redundancy_index = 0
    current_group_count = 0
    for tool in state:
        if tool == '#':
            current_group_count += 1
        elif current_group_count:
            if redundancy_index >= len(redundancy) or redundancy[redundancy_index] != current_group_count:
                return False
            redundancy_index += 1
            current_group_count = 0
    if current_group_count > 0 and redundancy_index < len(redundancy):
        return current_group_count == redundancy[redundancy_index]
    return True


def compute_possibility_count(known_state, redundancy):
    state = known_state.copy()
    (unknown_indices,) = np.nonzero(np.where(known_state == '?', 1, 0))
    broken_tool_count = sum(redundancy)
    remaining_broken_tool_count = broken_tool_count - \
        np.count_nonzero(np.where(known_state == '#', 1, 0))
    if remaining_broken_tool_count == 0:
        return int(len(redundancy) == 0)
    if remaining_broken_tool_count < 0:
        return 0
    count = 0
    # print(f'{known_state}, {redundancy}, {unknown_indices}, {remaining_broken_tool_count}')
    for comb in combinations(unknown_indices, remaining_broken_tool_count):
        state[unknown_indices] = '.'
        state[np.array(comb)] = '#'
        if is_state_possible(state, redundancy):
            # print(f"is possible: {''.join(state)}, {redundancy}")
            count += 1
    # print(f'count: {count}')
    return count


def compute_possibility_count_recursive(known_state, redundancy):
    print(f"start: ('{known_state}', {redundancy})")
    result = 0
    if len(known_state) == 0:
        result = int(len(redundancy) == 0)
    elif len(known_state) < 5:
        result = compute_possibility_count(
            np.array(list(known_state)), redundancy)

    else:
        m = len(known_state)//2
        if known_state[m] == '?':
            result = compute_possibility_count_recursive(known_state[:m] + '.' + known_state[m+1:], redundancy) \
                + compute_possibility_count_recursive(
                    known_state[:m] + '#' + known_state[m+1:], redundancy)
        elif known_state[m] == '.':
            left_side = known_state[:m]
            right_side = known_state[m+1:]
            result = 0
            for i in range(len(redundancy) + 1):
                left_result = compute_possibility_count_recursive(
                    left_side, redundancy[:i])
                if left_result > 0:
                    result += left_result * \
                        compute_possibility_count_recursive(
                            right_side, redundancy[i:])
        else:
            result = 0
            for i in range(len(redundancy)):
                left_redundancy = redundancy[:i]
                this_redundancy = redundancy[i]
                right_redundancy = redundancy[i + 1:]
                for j in range(this_redundancy):
                    start_index = m - j
                    end_index = start_index + this_redundancy
                    if start_index < 0 or end_index >= len(known_state):
                        continue
                    if any((tool == '.' for tool in known_state[start_index:end_index])):
                        continue
                    if start_index > 0 and known_state[start_index - 1] == '#':
                        continue
                    if end_index + 1 < len(known_state) and known_state[end_index + 1] == '#':
                        continue
                    left_side = known_state[:start_index -
                                            1] if start_index > 0 else ''
                    right_side = known_state[end_index +
                                             1:] if end_index + 1 < len(known_state) else ''
                    left_result = compute_possibility_count_recursive(
                        left_side, left_redundancy)
                    if left_result > 0:
                        result += left_result * \
                            compute_possibility_count_recursive(
                                right_side, right_redundancy)
    print(f"end: ('{known_state}', {redundancy}): {result}")
    return result


cache = {}


def compute_possibility_count_dp(known_state, redundancy):
    global cache
    if cache.get((known_state, redundancy)) is not None:
        return cache[(known_state, redundancy)]

    if len(known_state) == 0:
        cache[(known_state, redundancy)] = int(len(redundancy) == 0)
    elif len(redundancy) == 0:
        cache[(known_state, redundancy)] = 1 - int('#' in known_state)
    elif known_state[0] == '.':
        cache[(known_state, redundancy)] = compute_possibility_count_dp(
            known_state[1:], redundancy)
    elif known_state[0] == '#':
        if len(known_state) < redundancy[0] or '.' in known_state[1:redundancy[0]] or (known_state + '-')[redundancy[0]] == '#':
            cache[(known_state, redundancy)] = 0
        else:
            cache[(known_state, redundancy)] = compute_possibility_count_dp(
                known_state[redundancy[0] + 1:], redundancy[1:])
    else:
        cache[(known_state, redundancy)] = compute_possibility_count_dp('.' + known_state[1:], redundancy) \
            + compute_possibility_count_dp('#' + known_state[1:], redundancy)
    return cache[(known_state, redundancy)]


if __name__ == '__main__':
    solve_part1('example', 5)
