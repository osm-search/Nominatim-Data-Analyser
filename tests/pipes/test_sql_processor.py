from analyser.core.pipes.data_fetching import SQLProcessor
from psycopg2._psycopg import connection

def test_process_sql_processor(sql_processor: SQLProcessor, 
                               temp_db_conn: connection):
    """
        Test the process() method of the SQLProcessor.
    """
    with temp_db_conn.cursor() as temp_db_cursor:
        temp_db_cursor.execute('CREATE TABLE test_table(val VARCHAR(255));')
        temp_db_cursor.execute("""
            INSERT INTO test_table (val) VALUES ('test1'), ('test2'), ('test3');
        """)
    sql_processor.query = 'SELECT * FROM test_table'

    results = sql_processor.process(given_conn=temp_db_conn)
    assert len(results) == 3 and results[0]['val'] == 'test1' and results[1]['val'] == 'test2' and results[2]['val'] == 'test3'
