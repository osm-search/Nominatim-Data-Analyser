from __future__ import annotations
from abc import ABCMeta, abstractmethod

class Pipe(metaclass=ABCMeta):
    """
        This is the base class for every pipe.
    """
    def __init__(self) -> None:
        self._next_pipe = None

    def plug_pipe(self, pipe: Pipe) -> Pipe:
        self._next_pipe = pipe
        return pipe

    def process_and_next(self, data: any = None) -> any:
        """
            Process this pipe and process the next one
            by giving it the result of this execution.
        """
        result = self.process(data)
        if self._next_pipe:
            self._next_pipe.process_and_next(result)
        return None

    @abstractmethod
    def process(self, data: any = None) -> any:
        """
            Contains the execution logic of this pipe.
        """
        return
