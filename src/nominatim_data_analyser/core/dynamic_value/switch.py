from . import DynamicValue
from typing import Any


class Switch(DynamicValue):
    """
        Dynamic value implementing a switch condition.
        The value of the expression is evaluated against the
        cases to get the right value.
    """
    def __init__(self, expression: str, cases: dict[str, Any]) -> None:
        self.expression = expression
        self.cases = cases

    def resolve(self, data: dict[str, Any]) -> Any:
        if self.expression not in data:
            raise RuntimeError(f'The expression {self.expression} was not found '
                               'in the input dictionary.')

        if data[self.expression] not in self.cases:
            raise RuntimeError(f'The case {data[self.expression]} is not in '
                               f'the configured switch cases: {list(self.cases.keys())}')

        return self.cases[data[self.expression]]
