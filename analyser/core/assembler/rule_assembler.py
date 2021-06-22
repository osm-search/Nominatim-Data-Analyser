from __future__ import annotations
from analyser.core.deconstructor.yaml_rule_deconstructor import BACKTRACKING_EVENT, NEW_NODE_EVENT
from analyser.core.pipes import FillingPipe
from analyser.core.qa_rule import ExecutionContext
from analyser.core.deconstructor import YAMLRuleDeconstructor
from analyser.logger.logger import LOG
from collections import deque
from .pipe_factory import PipeFactory
from typing import Deque
import typing

if typing.TYPE_CHECKING:
    from analyser.core import Pipe

class RuleAssembler():
    """
        Get deconstruction informations from the 
        YAML deconstructor and assembles the rule's pipeline.
    """
    def __init__(self, yaml_name: str) -> None:
        self.yaml_name = yaml_name
        self.deconstructor: YAMLRuleDeconstructor = YAMLRuleDeconstructor(yaml_name)
        self.deconstructor.subscribe_event(NEW_NODE_EVENT, self.on_new_node)
        self.deconstructor.subscribe_event(BACKTRACKING_EVENT, self.on_backtrack)
        self.exec_context: ExecutionContext = ExecutionContext()
        self.first_pipe: Pipe = FillingPipe()
        self.nodes_history: Deque[Pipe] = deque()

    def on_new_node(self, node: dict) -> None:
        """
            Raised by the deconstructor when a new node
            is reached.
        """
        if node['type'] ==  'ROOT_NODE':
            self.nodes_history.append(self.first_pipe)
        else:
            pipe = PipeFactory.assemble_pipe(node, self.exec_context)
            #Plug the new pipe to the current last pipe of the deque
            self.nodes_history[-1].plug_pipe(pipe)
            LOG.info("%s | Assembler: %s plugged to %s", self.yaml_name, pipe, self.nodes_history[-1])
            self.nodes_history.append(pipe)

    def on_backtrack(self, backtrack_amount: int) -> None:
        """
            Raised by the deconstructor when backtrack is
            processed through the tree.
        """
        for _ in range(backtrack_amount):
            if self.nodes_history:
                self.nodes_history.pop()

    def assemble(self) -> Pipe:
        """
            Assembles the rule's pipeline
        """
        self.deconstructor.deconstruct()
        return self.first_pipe
