from typing import Any
import logging

from .. import Pipe
from ..pipes.filling_pipe import FillingPipe
from ..qa_rule import ExecutionContext
from .pipe_factory import PipeFactory

LOG = logging.getLogger()


class PipelineAssembler():
    """ Factory for creating a pipeline from a specification.
    """
    def __init__(self, rule_name: str) -> None:
        self.rule_name = rule_name

    def assemble(self, specification: list[Any]) -> Pipe:
        """
            Assembles a pipeline from the given specification.
        """
        exec_context: ExecutionContext = ExecutionContext()
        exec_context.rule_name = self.rule_name

        first_pipe: Pipe = FillingPipe({}, exec_context)
        prev_step = first_pipe

        for node in specification:
            pipe = PipeFactory.assemble_pipe(node, exec_context)
            prev_step.plug_pipe(pipe)
            LOG.debug("<%s> Assembler -> %s plugged to %s",
                      self.rule_name, pipe, prev_step)
            prev_step = pipe

        return first_pipe
