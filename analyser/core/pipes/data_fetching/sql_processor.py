from __future__ import annotations
from analyser.logger.timer import Timer
from .result_type import ResultType
from typing import Dict, List
from analyser.database.connection import connect
from analyser.core import Pipe
import importlib
import psycopg2.extras

class SQLProcessor(Pipe):
    """
        Handles the execution of an SQL query, converts
        the resulting data to the generic data model of the analyser
        and send them to the next pipe.
    """
    def on_created(self) -> None:
        self.query = self.extract_data('query')
        self.results_types: List[ResultType] = list()

        for result_type in self.extract_data('results_types', default=list()):
                #Create ResultType with additional argument if it is a dict
                if isinstance(result_type, dict):
                    str_type = next(iter(result_type))
                    arguments = result_type[str_type]
                    self.results_types.append(ResultType(str_type, arguments))
                else:
                    self.results_types.append(ResultType(result_type))

    def process(self, data: any = None) -> List[Dict]:
        """
            Executes the query and converts data based on
            the results_types given.
        """
        converted_results: List[Dict] = list()
        with connect() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                timer = Timer().start_timer()
                cur.execute(self.query)
                elapsed_mins, elapsed_secs = timer.get_elapsed()
                self.log(f'Query {self.id} executed in {elapsed_mins} mins {elapsed_secs} secs.')
                for data_result in cur:
                    converted_results.append(self.convert_results(data_result))
        self.log(f'Query {self.id} returned {len(converted_results)} results.')
        return converted_results

    def convert_results(self, results: Dict) -> Dict:
        """
            Converts the results to their corresponding elements.
        """
        module = importlib.import_module('analyser.core.model')
        for i, (k, v) in enumerate(results.items()):
            if i < len(self.results_types):
                dclass = getattr(module, self.results_types[i].str_type)
                convert = getattr(dclass, 'create_from_sql_result')
                results[k] = convert(v, *self.results_types[i].additional_arguments)
        return results
