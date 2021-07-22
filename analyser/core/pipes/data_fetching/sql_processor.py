from __future__ import annotations
from analyser.logger.timer import Timer
from typing import Dict, List
from analyser.database.connection import connect
from analyser.core import Pipe
import psycopg2.extras

class SQLProcessor(Pipe):
    """
        Handles the execution of an SQL query and 
        send the results to the next pipe.
    """
    def on_created(self) -> None:
        self.query = self.extract_data('query')

    def process(self, data: any = None) -> List[Dict]:
        """
            Executes the query and returns the results.
        """
        results: List = None
        with connect() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                timer = Timer().start_timer()
                cur.execute(self.query)
                results = list(cur)
                elapsed_mins, elapsed_secs = timer.get_elapsed()
                self.log(f'Query {self.id} executed in {elapsed_mins} mins {elapsed_secs} secs.')

        self.log(f'Query {self.id} returned {len(results)} results.')
        return results