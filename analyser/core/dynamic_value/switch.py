from analyser.core.dynamic_value import DynamicValue
from typing import Any, Dict

class Switch(DynamicValue):
    """
        Dynamic value implementing a switch condition.
        The value of the expression is evaluated against the
        cases to get the right value.
    """
    def __init__(self, expression: str, cases: Dict) -> None:
        self.expression = expression
        self.cases = cases

    def resolve(self, data: Dict) -> Any:
        if self.expression not in data:
            raise Exception(f'The expression {self.expression} was not found in the input dictionnary.')
        
        if data[self.expression] not in self.cases:
            raise Exception(f'The case {data[self.expression]} is not in the configured switch cases: {self.cases}')

        return self.cases[data[self.expression]]