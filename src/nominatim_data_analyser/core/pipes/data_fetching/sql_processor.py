from typing import Any

import psycopg

from ....config import Config
from ... import Pipe
from ....timer import Timer


class SQLProcessor(Pipe):
    """
        Handles the execution of an SQL query and
        send the results to the next pipe.
    """
    def on_created(self) -> None:
        self.query = self.extract_data('query', required=True)

    def process(self, _: Any) -> list[dict[str, Any]]:
        """
            Executes the query and returns the results.
        """
        results: list[dict[str, Any]]

        with psycopg.connect(Config.values['Dsn']) as conn:
            with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                timer = Timer(f'Query {self.id}')
                cur.execute(self.query)
                results = cur.fetchall()
                self.log(timer.elapsed_str)
            self.log(f'Query {self.id} returned {len(results)} results.')

        return results
