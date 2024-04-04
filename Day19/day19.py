import re
from parse import parse_file
from typing import List
from rule import Rule
from symbolic_variable_set import SymbolicVariableSet, NO_RESTRICTIONS


def parse_workflow(workflow_string):
    match = re.match("([a-z]+)\{(.+)\}", workflow_string)
    name = match.group(1)
    rules = match.group(2)
    rules = list(map(Rule.from_str, rules.split(',')))
    return (name, rules)


def parse_part_ratings(part_ratings_string):
    match = re.match(
        "\{(x)=([0-9]+),(m)=([0-9]+),(a)=([0-9]+),(s)=([0-9]+)\}", part_ratings_string)
    part_ratings = {match.group(i): int(match.group(i + 1))
                    for i in range(1, 9, 2)}
    return part_ratings


def parse_input(filename):
    input = parse_file(filename)
    split_index = input.index('')
    workflows = input[:split_index]
    workflows = {name: rules for (name, rules) in map(
        parse_workflow, workflows)}
    ratings = input[split_index + 1:]
    ratings = list(map(parse_part_ratings, ratings))
    return (workflows, ratings)


def compute_workflow(workflow: List[Rule], part_ratings) -> str:
    for rule in workflow:
        result = rule.compute_rule(part_ratings)
        if result is not None:
            return result


def is_part_accepted(workflows, part_ratings, start_workflow='in') -> bool:
    current_workflow = start_workflow
    while current_workflow != Rule.ACCEPTED and current_workflow != Rule.REJECTED:
        current_workflow = compute_workflow(
            workflows[current_workflow], part_ratings)
    return current_workflow == Rule.ACCEPTED


def solve_part1(filename):
    (workflows, ratings) = parse_input(filename)
    solution = 0
    for part_ratings in ratings:
        if is_part_accepted(workflows, part_ratings):
            solution += sum(part_ratings.values())
    print(solution)


def compute_accepted_possiblities(workflows, current_workflow, current_symbolic_variables: SymbolicVariableSet):
    if current_workflow == Rule.ACCEPTED:
        return current_symbolic_variables.count_possibilities()
    elif current_workflow == Rule.REJECTED:
        return 0
    elif not current_symbolic_variables.is_possible():
        return 0

    result = 0
    current_additional_constraints = NO_RESTRICTIONS
    for rule in workflows[current_workflow]:
        next_symbolic_variables = current_symbolic_variables.combine(
            current_additional_constraints)
        next_symbolic_variables = next_symbolic_variables.combine(
            rule.get_restriction_if_true())
        result += compute_accepted_possiblities(
            workflows, rule.resulting_workflow, next_symbolic_variables)
        current_additional_constraints = current_additional_constraints.combine(
            rule.get_restriction_if_false())
    return result


def solve_part2(filename):
    (workflows, _) = parse_input(filename)
    starting_constraints = SymbolicVariableSet(['x', 'm', 'a', 's'], [1, 4001])
    print(compute_accepted_possiblities(workflows, 'in', starting_constraints))


if __name__ == '__main__':
    solve_part1('input')
    solve_part2('input')
