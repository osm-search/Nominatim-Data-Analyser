from typing import Any
from ...core import Pipe

class FillingPipe(Pipe):
    """
        Pipe used only for filling.
        It doesn't do anything with data.
    """
    def process(self, data: Any = None) -> Any:
        """
            Contains the execution logic of this pipe.
        """
        return data
