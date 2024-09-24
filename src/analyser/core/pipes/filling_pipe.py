from __future__ import annotations
from analyser.core import Pipe

class FillingPipe(Pipe):
    """
        Pipe used only for filling.
        It doesn't do anything with data.
    """
    def process(self, data: any = None) -> any:
        """
            Contains the execution logic of this pipe.
        """
        return data