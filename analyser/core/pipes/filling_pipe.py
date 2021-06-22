from __future__ import annotations
from analyser.core.pipe import Pipe
import typing

if typing.TYPE_CHECKING:
    from analyser.core.qa_rule import ExecutionContext

class FillingPipe(Pipe):
    """
        Pipe used only for filling.
        It doesn't do anything with data.
    """
    def __init__(self) -> None:
        super().__init__()

    def process(self, data: any = None) -> any:
        """
            Contains the execution logic of this pipe.
        """
        return data

    @staticmethod
    def create_from_node_data(data: dict, exec_context: ExecutionContext) -> FillingPipe:
        """
            Assembles the pipe with the given node data.
        """
        return FillingPipe()