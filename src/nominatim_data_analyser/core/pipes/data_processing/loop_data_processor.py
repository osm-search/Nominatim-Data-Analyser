from typing import Any
from ....timer import Timer
from ... import Pipe


class LoopDataProcessor(Pipe):
    """
        Transforms each element of a list by processing them with a
        custom processing pipeline.
    """
    def on_created(self) -> None:
        self.processing_pipeline: Pipe = self.extract_data('sub_pipeline', required=True)

    def process(self, data: Any) -> list[Any]:
        """
            Processes each data of the input list with the processing pipeline.
        """
        if not isinstance(data, list):
            raise RuntimeError('Unexpected data input for loop data processor. Needs list.')

        timer = Timer('Loop data processor')
        processed_data = list()
        for d in data:
            processed_result = self.processing_pipeline.process_and_next(d, return_on_none=True)
            if processed_result:
                # The result can be a list with multiple results or only one result
                if isinstance(processed_result, list):
                    processed_data.extend(processed_result)
                else:
                    processed_data.append(processed_result)

        self.log(timer.elapsed_str)
        return processed_data
