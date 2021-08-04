import psycopg2
import pytest
from analyser.core.pipes import FillingPipe
from analyser.core.pipes.data_fetching.sql_processor import SQLProcessor
from analyser.core.pipes.data_processing import GeometryConverter
from analyser.core.pipes.output_formatters import (GeoJSONFeatureConverter,
                                                   GeoJSONFormatter)
from analyser.core.qa_rule import ExecutionContext
from analyser.database.connection import connect
from psycopg2._psycopg import connection, cursor


@pytest.fixture
def temp_db() -> str:
    """ 
        Create an empty database for the test.
    """
    name = 'test_qa_tool_python_unittest'
    conn = psycopg2.connect(database='postgres')

    conn.set_isolation_level(0)
    with conn.cursor() as cur:
        cur.execute('DROP DATABASE IF EXISTS {}'.format(name))
        cur.execute('CREATE DATABASE {}'.format(name))
    conn.close()

    yield name

    conn = psycopg2.connect(database='postgres')
    conn.set_isolation_level(0)
    with conn.cursor() as cur:
        cur.execute('DROP DATABASE IF EXISTS {}'.format(name))
    conn.close()

@pytest.fixture
def temp_db_conn(temp_db) -> connection:
    """
        Connection to the test database.
    """
    with connect('dbname=' + temp_db) as conn:
        yield conn

@pytest.fixture
def temp_db_cursor(temp_db) -> cursor:
    """     
        Connection and cursor towards the test database. 
        The connection will be in auto-commit mode.
    """
    conn = psycopg2.connect('dbname=' + temp_db)
    conn.set_isolation_level(0)
    with conn.cursor() as cur:
        yield cur
    conn.close()

@pytest.fixture
def dsn(temp_db):
    return 'dbname=' + temp_db

@pytest.fixture
def sql_processor(execution_context) -> SQLProcessor:
    return SQLProcessor({}, execution_context)

@pytest.fixture
def geometry_converter(execution_context) -> GeometryConverter:
    return GeometryConverter({
        'geometry_type': 'Node'
    }, execution_context)

@pytest.fixture
def filling_pipe(execution_context) -> FillingPipe:
    return FillingPipe({}, execution_context)

@pytest.fixture
def geojson_feature_converter(execution_context) -> GeoJSONFeatureConverter:
    return GeoJSONFeatureConverter({
        'properties': {
            'prop1': 'val1',
            'prop2': 'val2'
        }
    }, execution_context)

@pytest.fixture
def geojson_formatter(execution_context) -> GeoJSONFormatter:
    return GeoJSONFormatter({}, execution_context)

@pytest.fixture
def execution_context() -> ExecutionContext:
    exec_context = ExecutionContext()
    exec_context.rule_name = 'test_rule'
    return exec_context
