from . import DynamicValue
from typing import Any

class Variable(DynamicValue):
    """
        Dynamic value corresponding to a basic variable.
        The right value is extracted based on its key name.
    """
    def __init__(self, name: str) -> None:
        self.name = name

    def resolve(self, data: dict[str, Any]) -> Any:
        if self.name not in data:
            raise Exception(f'The variable name {self.name} was not found in the input dictionary.')

        return data[self.name]
