import re
from parse import parse_file
from sympy.solvers.diophantine.diophantine import base_solution_linear
from functools import reduce


def parse_input(filename):
    lines = parse_file(filename)
    instructions = lines[0]
    graph = {}  # Entry Node: (Left Exit Node, Right Exit Node)
    for line in lines[2:]:
        m = re.match('([0-9A-Z]{3}) = \(([0-9A-Z]{3}), ([0-9A-Z]{3})\)', line)
        if m is None:
            print(
                f'ParseError at matching {line} with "([0-9A-Z]{3}) = \(([0-9A-Z]{3}), ([0-9A-Z]{3})\)"')
            return

        graph[m.group(1)] = (m.group(2), m.group(3))
    return (instructions, graph)


def solve_part1(filename):
    (instructions, graph) = parse_input(filename)
    current_node = 'AAA'
    step_count = 0
    while current_node != 'ZZZ':
        for instruction in instructions:
            if instruction == 'L':
                current_node = graph[current_node][0]
            else:
                current_node = graph[current_node][1]
            step_count += 1
            if current_node == 'ZZZ':
                break
    print(step_count)


def get_run_metadata(instructions, graph, start_node):
    full_run = [start_node]
    node_buckets = [{} for _ in range(len(graph))]
    node_buckets[0][start_node] = 0
    period_repetition = 0
    pre_period_run = None
    period = None
    while pre_period_run is None:
        for (i, instruction) in enumerate(map(lambda i: 0 if i == 'L' else 1, instructions)):
            bucket = (i + 1) % len(instructions)
            if i + 1 == len(instructions):
                period_repetition += 1
            next_node = graph[full_run[-1]][instruction]
            if next_node in node_buckets[bucket]:
                index = len(instructions) * \
                    node_buckets[bucket][next_node] + bucket
                print(f'Expected: {next_node}, got: {full_run[index]}')
                pre_period_run = full_run[:index]
                period = full_run[index:]
                break
            else:
                full_run.append(next_node)
                node_buckets[bucket][next_node] = period_repetition

    pre_period_steps = len(pre_period_run)
    pre_period_winners = list(map(lambda i_node: i_node[0], filter(
        lambda i_node: i_node[1][2] == 'Z', enumerate(pre_period_run))))
    period_steps = len(period)
    period_winners = list(map(lambda i_node: i_node[0], filter(
        lambda i_node: i_node[1][2] == 'Z', enumerate(period))))
    return (pre_period_steps, pre_period_winners, period_steps, period_winners)


def combine_period_tables(period_table1, period_table2):
    # k: pre_period_steps, A: pre_period_destination_occurences, n: period_steps, B: period_destination_occurences
    print(period_table1)
    print(period_table2)
    (k, A, n, B) = period_table1
    (l, C, m, D) = period_table2
    if l < k:
        return combine_period_tables(period_table2, period_table1)
    elif k < l:
        for i in range(len(B)):
            if B[i] < l - k:
                A.append(B[i] + k)
                B[i] += n - l + k
            else:
                B[i] -= l - k
        k = l
    (s, X, t, Y) = (k, [], lcm(n, m), [])
    for a in A:
        if a in C:
            X.append(a)
    g = None
    for b in B:
        for d in D:
            (x_0, _) = solve_diophantine(d - b, n, -m)
            if x_0 is None:
                continue
            x_0 = x_0 % m
            if x_0 < 0:
                x_0 += m
            Y.append(x_0 * n + b)
    return (s, X, t, Y)


def solve_diophantine(n, m, d):
    # Solves the diophantine equation x*n + y*m = d and returns a tuple containing (g, x_0, y_0) where g = gcd(n, m)
    # and (x_0, y_0) is the integer solution where x_0 is the least positive integer possible

    # assume |n| > |m|,
    # n = q_1 * m + r_1         | r_1 = 1*n + (-q_1) * m
    # m = q_2 * r_1 + r_2       | r_2 = 1*m + (-q_2) * r_1 = 1 * m + (-q_2) * (1 * n + (-q_1) * m) = (-q_2) * n + (q_1 * q_2 + 1) * m
    # r_1 = q_3 * r_2 + r_3
    # ...
    # r_n-1 = q_n * r_n + 0
    # ==> r_n = gcd(n, m)
    return base_solution_linear(n, m, d)


def gcd(n, m):
    (n, m) = (abs(n), abs(m))
    if n < m:
        (n, m) = (m, n)
    while m != 0:
        (n, m) = (m, n % m)
    return n


def lcm(n, m):
    return n * m // gcd(n, m)


def solve_part2(filename):
    (instructions, graph) = parse_input(filename)
    start_nodes = list(filter(lambda node: node[2] == 'A', graph.keys()))
    period_tables = [get_run_metadata(instructions, graph, start_node)
                     for start_node in start_nodes]
    final_period_table = reduce(
        combine_period_tables, period_tables[1:], period_tables[0])
    print(final_period_table)


if __name__ == '__main__':
    solve_part1('input')
    solve_part2('example')
    solve_part2('input')
