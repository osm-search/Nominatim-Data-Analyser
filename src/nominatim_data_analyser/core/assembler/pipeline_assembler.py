from typing import Any
from ..deconstructor import PipelineDeconstructor, BACKTRACKING_EVENT, NEW_NODE_EVENT
from .. import Pipe
from ..pipes import FillingPipe
from ..qa_rule import ExecutionContext
from ...logger.logger import LOG
from collections import deque
from .pipe_factory import PipeFactory


class PipelineAssembler():
    """
        Get deconstruction informations from the
        pipeline deconstructor and assembles the final pipeline.
    """
    def __init__(self, pipeline_specification: dict[str, Any], rule_name: str) -> None:
        self.rule_name = rule_name
        self.deconstructor: PipelineDeconstructor = PipelineDeconstructor(pipeline_specification, rule_name)
        self.deconstructor.subscribe_event(NEW_NODE_EVENT, self.on_new_node)
        self.deconstructor.subscribe_event(BACKTRACKING_EVENT, self.on_backtrack)
        self.nodes_history: deque[Pipe] = deque()
        self.exec_context: ExecutionContext = ExecutionContext()
        self.exec_context.rule_name = rule_name
        self.first_pipe: Pipe = FillingPipe({}, self.exec_context)

    def on_new_node(self, node: dict[str, Any]) -> None:
        """
            Raised by the deconstructor when a new node
            is reached.
        """
        if node['type'] == 'ROOT_NODE':
            self.nodes_history.append(self.first_pipe)
        else:
            pipe = PipeFactory.assemble_pipe(node, self.exec_context)
            # Plug the new pipe to the current last pipe of the deque
            self.nodes_history[-1].plug_pipe(pipe)
            LOG.info("<%s> Assembler -> %s plugged to %s", self.rule_name, pipe, self.nodes_history[-1])
            self.nodes_history.append(pipe)

    def on_backtrack(self) -> None:
        """
            Raised by the deconstructor when backtrack is
            processed through the tree.
        """
        if self.nodes_history:
            self.nodes_history.pop()

    def assemble(self) -> Pipe:
        """
            Assembles the full pipeline.
        """
        self.deconstructor.deconstruct()
        return self.first_pipe
