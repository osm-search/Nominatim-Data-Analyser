from __future__ import annotations
from typing import List, Any
from ....logger.timer import Timer
from ... import Pipe

class LoopDataProcessor(Pipe):
    """
        Transforms each element of a list by processing them with a
        custom processing pipeline.
    """
    def on_created(self) -> None:
        self.processing_pipeline: Pipe = self.extract_data('sub_pipeline', required=True)

    def process(self, data: List[Any]) -> List[Any]:
        """
            Processes each data of the input list with the processing pipeline.
        """
        timer = Timer().start_timer()
        processed_data = list()
        for d in data:
            processed_result = self.process_one_data(d)
            if processed_result:
                #The result can be a list with multiple results or only one result
                if isinstance(processed_result, List):
                    processed_data.extend(processed_result)
                else:
                    processed_data.append(processed_result)
    
        elapsed_mins, elapsed_secs = timer.get_elapsed()
        self.log(f'Loop data processor executed in {elapsed_mins} mins {elapsed_secs} secs.')
        return processed_data

    def process_one_data(self, data: Any) -> Any:
        """
            Processes one data through each pipe of the processing pipeline.
            If one pipe returns None the process is stopped and None is returned.
        """
        current_pipe: Pipe | None = self.processing_pipeline
        while current_pipe:
            data = current_pipe.process(data)
            if data is None:
                break
            current_pipe = next(iter(current_pipe.next_pipes), None)
        return data
