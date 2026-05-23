from typing import Any
import uuid
import logging

from abc import ABC, abstractmethod
from .exceptions import YAMLSyntaxException
from .qa_rule import ExecutionContext


LOG = logging.getLogger()


class Pipe(ABC):
    """
        This is the base class for every pipe.
    """
    def __init__(self, data: dict[str, Any], exec_context: ExecutionContext) -> None:
        self.id = uuid.uuid1()
        self.exec_context = exec_context
        self.data = data
        self.next_pipe: Pipe | None = None
        self.on_created()

    def plug_pipe(self, pipe: 'Pipe') -> 'Pipe':
        """
            Plugs a pipe to the current pipe and returns the
            plugged pipe.
        """
        assert self.next_pipe is None
        self.next_pipe = pipe
        return pipe

    def process_and_next(self, data: Any = None, return_on_none: bool = False) -> Any:
        """
            Process this pipe and process the plugged ones
            by giving them the result of this execution.
        """
        result = self.process(data)

        if result is None and return_on_none:
            return None

        if self.next_pipe is not None:
            result = self.next_pipe.process_and_next(result)

        return result

    def __str__(self) -> str:
        return type(self).__name__ + ' ' + str(self.id)

    @abstractmethod
    def process(self, data: Any) -> Any:
        """
            Contains the execution logic of this pipe.
        """

    def on_created(self) -> None:
        """
            This method is called when the pipe is created.

            It should be overriden by the child pipe if any action is needed
            at the creation.

            This is needed because child pipes can't have their own
            constructor since pipes are created dynamically.
        """
        pass

    def extract_data(self, name: str, default: Any = None, required: bool = False) -> Any:
        """
            Tries to get data from the data dictionary.

            If the data name provided exists in the dictionary it gets pop
            out and it gets returned. But if it doesn't exist, the default
            value provided is returned (None by default).

            if the required value is set to True and if the data can't be
            found, a YAMLSyntaxException is raised.
        """
        if name in self.data:
            return self.data.pop(name)
        if not required:
            return default

        raise YAMLSyntaxException(
            f'The field "{name}" is required for the pipe of type {type(self).__name__}')

    def log(self, msg: str, level: int = logging.INFO) -> None:
        """
            Log the given message with the given log level (default is INFO).
            The rule name is automatically prefixed to the log message.
        """
        LOG.log(level, f'<{self.exec_context.rule_name if self.exec_context else "None"}> {msg}')
