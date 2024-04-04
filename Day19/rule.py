from typing import Literal, Optional
from symbolic_variable_set import SymbolicVariableSet, NO_RESTRICTIONS, IMPOSSIBLE


class Rule:
    ALWAYS = 0
    LESS_THAN = 1
    GREATER_THAN = 2

    OPERATION_TO_TYPE = {'<': LESS_THAN, '>': GREATER_THAN}
    TYPE_TO_OPERATION = {LESS_THAN: '<', GREATER_THAN: '>'}

    ACCEPTED = 'A'
    REJECTED = 'R'

    def __init__(self, type=Literal[0, 1, 2], resulting_workflow=str,
                 rating_key: Optional[Literal['x', 'm', 'a', 's']] = None,
                 compare_to: Optional[int] = None):
        self.type = type
        self.resulting_workflow = resulting_workflow
        self.rating_key = rating_key
        self.compare_to = compare_to

    def __repr__(self):
        if self.type == Rule.ALWAYS:
            return f'{self.resulting_workflow}'

        return f'{self.rating_key}{Rule.TYPE_TO_OPERATION[self.type]}{self.compare_to}:{self.resulting_workflow}'

    def compute_rule(self, part_ratings) -> Optional[str]:
        if self.type == Rule.ALWAYS:
            return self.resulting_workflow

        result = None
        if self.type == Rule.LESS_THAN:
            if part_ratings[self.rating_key] < self.compare_to:
                result = self.resulting_workflow
        elif self.type == Rule.GREATER_THAN:
            if part_ratings[self.rating_key] > self.compare_to:
                result = self.resulting_workflow
        return result

    def from_str(string):
        type = Rule.ALWAYS
        resulting_workflow = string
        rating_key = None
        compare_to = None
        for operation in ['<', '>']:
            if not operation in string:
                continue

            type = Rule.OPERATION_TO_TYPE[operation]
            (rating_key, rest) = string.split(operation)
            (compare_to, resulting_workflow) = rest.split(':')
            compare_to = int(compare_to)
        return Rule(type, resulting_workflow, rating_key, compare_to)

    def get_restriction_if_true(self) -> SymbolicVariableSet:
        if self.type == Rule.ALWAYS:
            return NO_RESTRICTIONS
        elif self.type == Rule.LESS_THAN:
            return SymbolicVariableSet([self.rating_key], [None, self.compare_to])
        elif self.type == Rule.GREATER_THAN:
            return SymbolicVariableSet([self.rating_key], [self.compare_to + 1, None])

    def get_restriction_if_false(self) -> SymbolicVariableSet:
        if self.type == Rule.ALWAYS:
            return IMPOSSIBLE
        elif self.type == Rule.LESS_THAN:
            return SymbolicVariableSet([self.rating_key], [self.compare_to, None])
        elif self.type == Rule.GREATER_THAN:
            return SymbolicVariableSet([self.rating_key], [None, self.compare_to + 1])
