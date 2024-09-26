from nominatim_data_analyser.core.pipes.data_fetching import SQLProcessor
from nominatim_data_analyser.config import Config


def test_on_created_sql_processor(sql_processor: SQLProcessor):
    """
        Test the on_created() method of the SQLProcessor.
    """
    sql_processor.query = None
    sql_processor.data['query'] = 'QUERY'
    sql_processor.on_created()
    assert sql_processor.query == 'QUERY'

def test_execute_query(sql_processor: SQLProcessor, dsn, temp_db_cursor):
    """
        Test the execute_query() method of the SQLProcessor.
    """
    temp_db_cursor.execute('CREATE TABLE test_table(val VARCHAR(255));')
    temp_db_cursor.execute("""
        INSERT INTO test_table (val) VALUES ('test1'), ('test2'), ('test3');
    """)
    sql_processor.query = 'SELECT * FROM test_table'

    Config.values['Dsn'] = dsn
    results = sql_processor.process(None)
    assert len(results) == 3 and results[0]['val'] == 'test1' and results[1]['val'] == 'test2' and results[2]['val'] == 'test3'
