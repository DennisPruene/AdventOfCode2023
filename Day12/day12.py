from parse import parse_file, extract_integers
from itertools import combinations
import numpy as np


def parse_line(line):
    (known_state, redundancy) = line.split(' ')
    redundancy = extract_integers(redundancy)
    return (known_state, redundancy)


def solve_part1(filename, repeat=1):
    tool_chart = parse_file(filename, parse_line)
    print(tool_chart)
    # solution = sum((compute_possibility_count(known_state, redundancy)
    #                for (known_state, redundancy) in tool_chart))
    # print(solution)
    solution = 0
    for (i, (known_state, redundancy)) in enumerate(tool_chart):
        if i % 100 == 0:
            print(f'{(i/len(tool_chart)) * 100}% completed')
        known_state = '?'.join([known_state] * repeat)
        solution += compute_possibility_count_recursive(
            known_state, redundancy * repeat)

        # print(f'{known_state}, {redundancy * repeat}, {cur_count}')
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
        return 1
    count = 0
    print(f'{known_state}, {redundancy}, {unknown_indices}, {remaining_broken_tool_count}')
    for comb in combinations(unknown_indices, remaining_broken_tool_count):
        state[unknown_indices] = '.'
        state[np.array(comb)] = '#'
        if is_state_possible(state, redundancy):
            print(f"is possible: {''.join(state)}, {redundancy}")
            count += 1
    print(f'count: {count}')
    return count


def compute_group_masks(working_mask, broken_mask, word_length, redundancy):
    minimal_start_indices = []
    maximal_end_indices = []
    for i in range(len(redundancy)):
        if i == 0:
            current_start_index = 0
        else:
            current_start_index = minimal_start_indices[i -
                                                        1] + redundancy[i-1] + 1
        current_mask = ((1 << redundancy[i]) - 1) << current_start_index
        while current_mask & working_mask:
            pass


def compute_possibility_count_recursive(known_state, redundancy):
    if len(known_state) == 0:
        return int(len(redundancy) == 0)
    if known_state[0] == '.':
        return compute_possibility_count_recursive(known_state[1:], redundancy)
    elif known_state[0] == '#':
        if len(redundancy) == 0:
            return 0
        if len(known_state) == 1:
            return int(len(redundancy) == 1 and redundancy[0] == 1)
        elif known_state[1] == '.':
            if redundancy[0] != 1:
                return 0
            return compute_possibility_count_recursive(known_state[2:], redundancy[1:])
        elif known_state[1] == '#':
            return compute_possibility_count_recursive(known_state[1:], [redundancy[0] - 1] + redundancy[1:])
        else:
            if redundancy[0] == 1:
                return compute_possibility_count_recursive(known_state[2:], redundancy[1:])
            else:
                return compute_possibility_count_recursive('#' + known_state[2:], [redundancy[0] - 1] + redundancy[1:])
    else:
        return compute_possibility_count_recursive('.' + known_state[1:], redundancy) + compute_possibility_count_recursive('#' + known_state[1:], redundancy)


if __name__ == '__main__':
    solve_part1('input', 5)
