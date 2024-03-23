import re
from parse import parse_file
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
    periods = [table[2] for table in period_tables]
    solution = reduce(lcm, periods, 1)
    print(solution)


if __name__ == '__main__':
    solve_part1('input')
    solve_part2('example')
    solve_part2('input')
