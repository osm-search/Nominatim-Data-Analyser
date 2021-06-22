from __future__ import annotations
from typing import List
import typing

if typing.TYPE_CHECKING:
    from analyser.core.pipes import SQLProcessor

class ExecutionContext():
    """
        Execution context of a QA Rule pipeline
        contains data and objects transfered through
        the pipeline execution.
    """
    def __init__(self) -> None:
        self.sql_processors: List[SQLProcessor] = []
        