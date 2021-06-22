from __future__ import annotations
from analyser.core.exceptions import YAMLSyntaxException
from analyser.core import Pipe
import importlib
import typing

if typing.TYPE_CHECKING:
    from analyser.core.qa_rule import ExecutionContext

class AdvancedLogicalUnit(Pipe):
    """
        Used to write custom code for a more
        advanced logic needed in a rule.
    """
    def __init__(self, exec_context: ExecutionContext) -> None:
        super().__init__(exec_context)

    @staticmethod
    def create_from_node_data(data: dict, exec_context: ExecutionContext) -> Pipe:
        """
            Assembles the pipe with the given node data.
        """
        module = importlib.import_module('analyser.core.pipes.advanced_logical_units')
        try:
            return getattr(module, data['name'])(exec_context)
        except AttributeError:
            raise YAMLSyntaxException("The advanced logical unit {} doesn't exist.".format(data['name']))