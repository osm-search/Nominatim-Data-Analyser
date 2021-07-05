from __future__ import annotations
from analyser.logger.logger import LOG
from analyser.logger.timer import Timer
from .result_type import ResultType
from analyser.core.model import Element
from typing import Dict, List
from analyser.database.connection import connect
from analyser.core import Pipe
import importlib
import psycopg2.extras
import typing

if typing.TYPE_CHECKING:
    from analyser.core.qa_rule import ExecutionContext

class SQLProcessor(Pipe):
    """
        Handles the execution of an SQL query, converts
        the resulting data to the generic data model of the analyser
        and send them to the next pipe.
    """
    def __init__(self, query: str, results_types: List[ResultType], exec_context: ExecutionContext) -> None:
        super().__init__(exec_context)
        self.query = query
        self.results_types = results_types

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
                LOG.info('Query %s executed in %s mins %s secs', self.id, *timer.get_elapsed())
                for data_result in cur:
                    converted_results.append(self.convert_results(data_result))
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
            
    @staticmethod
    def create_from_node_data(data: dict, exec_context: ExecutionContext) -> SQLProcessor:
        """
            Assembles the pipe with the given node data.
        """
        results_types: List[ResultType] = list()
        if 'results_types' in data:
            for d in data['results_types']:
                #Create ResultType with additional argument if it is a dict
                if isinstance(d, dict):
                    str_type = next(iter(d))
                    arguments = d[str_type]
                    results_types.append(ResultType(str_type, arguments))
                else:
                    results_types.append(ResultType(d))
        return SQLProcessor(data['query'], results_types, exec_context)

