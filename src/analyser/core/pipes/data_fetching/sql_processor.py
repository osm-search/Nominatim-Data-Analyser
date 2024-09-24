from __future__ import annotations

from typing import Dict, List

import psycopg2.extras
from ....config.config import Config
from ... import Pipe
from ....database.connection import connect
from ....logger.timer import Timer
from psycopg2._psycopg import connection


class SQLProcessor(Pipe):
    """
        Handles the execution of an SQL query and 
        send the results to the next pipe.
    """
    def on_created(self) -> None:
        self.query = self.extract_data('query', required=True)

    def process(self, data: any = None) -> List[Dict]:
        """
            Executes the query and returns the results.
        """
        with connect(Config.values['Dsn']) as conn:
            return self.execute_query(conn)
    
    def execute_query(self, conn: connection) -> List[Dict]:
        """
            Executes the query and returns the results.
            Takes a database connection as input.
        """
        results: List = None
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            timer = Timer().start_timer()
            cur.execute(self.query)
            results = list(cur)
            elapsed_mins, elapsed_secs = timer.get_elapsed()
            self.log(f'Query {self.id} executed in {elapsed_mins} mins {elapsed_secs} secs.')
        self.log(f'Query {self.id} returned {len(results)} results.')
        return results
