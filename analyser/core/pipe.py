from __future__ import annotations
from abc import ABCMeta, abstractmethod
import typing
import uuid

if typing.TYPE_CHECKING:
    from analyser.core.qa_rule import ExecutionContext

class Pipe(metaclass=ABCMeta):
    """
        This is the base class for every pipe.
    """
    def __init__(self, exec_context: ExecutionContext = None) -> None:
        self.id = uuid.uuid1()
        self.exec_context = exec_context
        self._next_pipes = set()

    def plug_pipe(self, pipe: Pipe) -> Pipe:
        self._next_pipes.add(pipe)
        return pipe

    def process_and_next(self, data: any = None) -> any:
        """
            Process this pipe and process the plugged ones
            by giving them the result of this execution.
        """
        result = self.process(data)
        for pipe in self._next_pipes:
            pipe.process_and_next(result)
        return None

    def __str__(self):
        return type(self).__name__ + ' ' + str(self.id)

    @abstractmethod
    def process(self, data: any = None) -> any:
        """
            Contains the execution logic of this pipe.
        """
        return

    @staticmethod
    @abstractmethod
    def create_from_node_data(data: dict, exec_context: ExecutionContext) -> Pipe:
        """
            Assembles the pipe with the given node data.
        """
        return
