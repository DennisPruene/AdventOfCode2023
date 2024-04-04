from typing import Union, List, Optional

MAX_INT = 2**31 - 1


class SymbolicVariableSet:
    def __init__(self, variable_names: List[str], intervals: Union[List[Optional[int]], List[List[Optional[int]]]]):
        if len(variable_names) == 0:
            self.symbolic_variables = {}
            return

        if isinstance(intervals[0], int) or intervals[0] is None:
            intervals = [intervals.copy() for _ in range(len(variable_names))]
        for interval in intervals:
            if interval[0] is None:
                interval[0] = 0
            if interval[1] is None:
                interval[1] = MAX_INT

        self.symbolic_variables = {variable_name: interval for (
            variable_name, interval) in zip(variable_names, intervals)}

    def __repr__(self) -> str:
        def repr_symbolic_variable(symbolic_variable):
            (variable_name, interval) = symbolic_variable
            return f'{interval[0]} <= {variable_name} < {interval[1]}'

        return f'[{", ".join(map(repr_symbolic_variable, self.symbolic_variables.items()))}]'

    def copy(self):
        return SymbolicVariableSet(
            list(self.symbolic_variables.keys()), list(map(list.copy, self.symbolic_variables.values())))

    def combine(self, other):
        result = self.copy()
        for (variable, (greater_equal_than, less_than)) in other.symbolic_variables.items():
            if variable not in result.symbolic_variables:
                result.symbolic_variables[variable] = [
                    greater_equal_than, less_than]
                continue

            interval = result.symbolic_variables[variable]
            if greater_equal_than > interval[0]:
                interval[0] = greater_equal_than
            if less_than < interval[1]:
                interval[1] = less_than
        return result

    def is_possible(self):
        for (greater_equal_than, less_than) in self.symbolic_variables.values():
            if less_than <= greater_equal_than:
                return False
        return True

    def count_possibilities(self):
        if not self.is_possible():
            return 0

        result = 1
        for (greater_equal_than, less_than) in self.symbolic_variables.values():
            result *= less_than - greater_equal_than
        return result


NO_RESTRICTIONS = SymbolicVariableSet([], [None, None])
IMPOSSIBLE = SymbolicVariableSet(['_'], [0, 0])
