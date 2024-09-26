from typing import Any, cast
from ..exceptions import YAMLSyntaxException
from .. import pipes as pipes_module
from .. import Pipe
from ..qa_rule import ExecutionContext

class PipeFactory():
    """
        Factory to assemble pipes.
    """
    @staticmethod
    def assemble_pipe(node_data: dict[str, Any], exec_context: ExecutionContext) -> Pipe:
        """
            Instantiate a pipe based on the given node_data
        """
        if 'type' not in node_data:
            raise YAMLSyntaxException("Each node of the tree (pipe) should have a type defined.")

        try:
            assembled_pipe = cast(Pipe, getattr(pipes_module, node_data['type'])(node_data, exec_context))
        except AttributeError:
            raise YAMLSyntaxException(f"The type {node_data['type']} doesn't exist.")

        return assembled_pipe
