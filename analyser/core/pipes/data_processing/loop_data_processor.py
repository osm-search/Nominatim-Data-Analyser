from __future__ import annotations
from analyser.core import Pipe
from typing import List

class LoopDataProcessor(Pipe):
    """
        Transforms each element of a list by processing them with a
        custom processing pipeline.
    """
    def on_created(self) -> None:
        self.processing_pipeline = self.extract_data('sub_pipeline', required=True)

    def process(self, data: List[any]) -> List[any]:
        """
            Processes each data of the input list with the processing pipeline.
        """
        return list(map(lambda x: self.processing_pipeline.process_and_next(x), data))