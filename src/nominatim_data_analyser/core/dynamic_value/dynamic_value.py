from abc import ABCMeta, abstractmethod
from typing import Any

class DynamicValue(metaclass=ABCMeta):
    """
        Base class for every DynamicValue type.

        A DynamicValue is meant to be created from a special type in the
        YAML Specification and it allows to replace some fields
        dynamically depending on the data values.
    """
    @abstractmethod
    def resolve(self, data: dict[str, Any]) -> Any:
        """
            Assigns a concrete value to the dynamic value
            based on the input data dictionnary.
        """
        return
