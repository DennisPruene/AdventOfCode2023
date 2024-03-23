from parse import parse_file, extract_integers
from math import factorial


def compute_sequence_derivative(seq):
    return [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]


def compute_all_derivatives(seq):
    seq_block = [seq]
    while any(seq_block[-1]):
        seq_block.append(compute_sequence_derivative(seq_block[-1]))
    return seq_block


def advance_block(seq_block):
    seq_block[-1].append(0)
    for (current_seq, derivative) in zip(reversed(seq_block[:-1]), reversed(seq_block[1:])):
        current_seq.append(current_seq[-1] + derivative[-1])


def advance_block_backwards(seq_block):
    seq_block[-1].insert(0, 0)
    for (current_seq, derivative) in zip(reversed(seq_block[:-1]), reversed(seq_block[1:])):
        current_seq.insert(0, current_seq[0] - derivative[0])


def get_seq_parametrization(seq_block):
    return [kth_deriv[0] for kth_deriv in seq_block[:-1]]


def binom(n, k):
    if k > n:
        return 0
    return factorial(n) // (factorial(k) * factorial(n - k))


def compute_seq_value(seq_param, n):
    return sum((binom(n, k)*seq_param[k] for k in range(len(seq_param))))


def solve_part1(filename):
    value_histories = parse_file(filename, extract_integers)
    value_seq_blocks = list(map(compute_all_derivatives, value_histories))
    solution = 0
    for value_seq_block in value_seq_blocks:
        advance_block(value_seq_block)
        solution += value_seq_block[0][-1]
    print(solution)


def solve_part2(filename):
    value_histories = parse_file(filename, extract_integers)
    value_seq_blocks = list(map(compute_all_derivatives, value_histories))
    solution = 0
    for value_seq_block in value_seq_blocks:
        advance_block_backwards(value_seq_block)
        solution += value_seq_block[0][0]
    print(solution)


if __name__ == '__main__':
    solve_part1('input')
    example_seq = [1, 3, 6, 10, 15, 21, 28]
    example_seq_block = compute_all_derivatives(example_seq)
    advance_block_backwards(example_seq_block)
    print(example_seq_block)
    solve_part2('input')
