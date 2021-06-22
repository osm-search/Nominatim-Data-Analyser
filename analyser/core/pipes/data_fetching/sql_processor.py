from __future__ import annotations
from analyser.core.model.element import Element
from typing import List
from analyser.database.connection import connect
from analyser.core.pipe import Pipe
import importlib
import typing

if typing.TYPE_CHECKING:
    from analyser.core.qa_rule import ExecutionContext

class SQLProcessor(Pipe):
    """
        Handles the execution of an SQL query, converts
        the resulting data to the generic data model of the analyser
        and send them to the next pipe.
    """
    def __init__(self, query: str, results_types: List[str], exec_context: ExecutionContext) -> None:
        super().__init__(exec_context)
        self.query = query
        self.results_types = results_types

    def process(self, data: any = None) -> List[List[Element]]:
        """
            Executes the query and converts data based on
            the results_types given.
        """
        converted_results = list()
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute(self.query)
                for data_result in cur:
                    converted_results.append(self.convert_results(data_result))
        return converted_results

    def convert_results(self, results: List[any]) -> List[Element]:
        """
            Converts the results to their corresponding elements.
        """
        module = importlib.import_module('analyser.core.model')
        converted_results = list()
        for i, result in enumerate(results):
            dclass = getattr(module, self.results_types[i])
            convert = getattr(dclass, 'create_from_sql_result')
            converted_results.append(convert(result))
        return converted_results
            
    @staticmethod
    def create_from_node_data(data: dict, exec_context: ExecutionContext) -> SQLProcessor:
        """
            Assembles the pipe with the given node data.
        """
        return SQLProcessor(data['query'], data['outputs_types'], exec_context)

