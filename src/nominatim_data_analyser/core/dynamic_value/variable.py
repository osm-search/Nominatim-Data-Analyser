from . import DynamicValue
from typing import Any, Dict

class Variable(DynamicValue):
    """
        Dynamic value corresponding to a basic variable.
        The right value is extracted based on its key name.
    """
    def __init__(self, name: str) -> None:
        self.name = name

    def resolve(self, data: Dict) -> Any:
        if self.name not in data:
            raise Exception(f'The variable name {self.name} was not found in the input dictionnary.')

        return data[self.name]
