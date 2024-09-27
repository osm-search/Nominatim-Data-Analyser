import sys
import sysconfig
from pathlib import Path

import psycopg
from psycopg import sql as pysql
import pytest

SRC_DIR = Path(__file__, '..', '..').resolve()

BUILD_DIR = f"build/lib.{sysconfig.get_platform()}-{sys.version_info[0]}.{sys.version_info[1]}"

if not (SRC_DIR / BUILD_DIR).exists():
    BUILD_DIR = f"build/lib.{sysconfig.get_platform()}-{sys.implementation.cache_tag}"

if (SRC_DIR / BUILD_DIR).exists():
    sys.path.insert(0, str(SRC_DIR / BUILD_DIR))


from nominatim_data_analyser.config import Config, load_config
from nominatim_data_analyser.core.pipes import FillingPipe
from nominatim_data_analyser.core.pipes.data_fetching.sql_processor import SQLProcessor
from nominatim_data_analyser.core.pipes.data_processing import (GeometryConverter,
                                                 LoopDataProcessor)
from nominatim_data_analyser.core.pipes.output_formatters import (GeoJSONFeatureConverter,
                                                   GeoJSONFormatter,
                                                   OsmoscopeLayerFormatter,
                                                   VectorTileFormatter)
from nominatim_data_analyser.core.qa_rule import ExecutionContext


@pytest.fixture
def temp_db() -> str:
    """ 
        Create an empty database for the test.
    """
    name = 'test_qa_tool_python_unittest'
    with psycopg.connect(dbname='postgres', autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute(pysql.SQL('DROP DATABASE IF EXISTS') + pysql.Identifier(name))
            cur.execute(pysql.SQL('CREATE DATABASE') + pysql.Identifier(name))

    yield name

    with psycopg.connect(dbname='postgres', autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute(pysql.SQL('DROP DATABASE IF EXISTS') + pysql.Identifier(name))

@pytest.fixture
def dsn(temp_db: str) -> str:
    return 'dbname=' + temp_db

@pytest.fixture
def temp_db_conn(dsn: str):
    """
        Connection to the test database.
    """
    with psycopg.connect(dsn) as conn:
        yield conn

@pytest.fixture
def temp_db_cursor(dsn: str):
    """ 
        Connection and cursor towards the test database. 
        The connection will be in auto-commit mode.
    """
    with psycopg.connect(dsn, autocommit=True) as conn:
        with conn.cursor() as cur:
            yield cur

@pytest.fixture
def config() -> Config:
    """
        Loads the config and returns it.
    """
    load_config(None)
    return Config

@pytest.fixture
def sql_processor(execution_context: ExecutionContext) -> SQLProcessor:
    return SQLProcessor({
        'query': 'dumb_query'
    }, execution_context)

@pytest.fixture
def geometry_converter(execution_context: ExecutionContext) -> GeometryConverter:
    return GeometryConverter({
        'geometry_type': 'Node'
    }, execution_context)

@pytest.fixture
def filling_pipe(execution_context: ExecutionContext) -> FillingPipe:
    return FillingPipe({}, execution_context)

@pytest.fixture
def geojson_feature_converter(execution_context: ExecutionContext) -> GeoJSONFeatureConverter:
    return GeoJSONFeatureConverter({
        'properties': [
            {'prop1': 'val1'},
            {'prop2': 'val2'}
        ]
    }, execution_context)

@pytest.fixture
def geojson_formatter(execution_context: ExecutionContext) -> GeoJSONFormatter:
    return GeoJSONFormatter({}, execution_context)

@pytest.fixture
def osmoscope_layer_formatter(execution_context: ExecutionContext) -> OsmoscopeLayerFormatter:
    return OsmoscopeLayerFormatter({
        'data_format_url': 'geojson_url'
    }, execution_context)

@pytest.fixture
def vector_tile_formatter(execution_context: ExecutionContext) -> VectorTileFormatter:
    return VectorTileFormatter({}, execution_context)

@pytest.fixture
def loop_data_processor(execution_context: ExecutionContext,
                        filling_pipe: FillingPipe) -> LoopDataProcessor:
    return LoopDataProcessor({
        'sub_pipeline': filling_pipe
    }, execution_context)

@pytest.fixture
def execution_context() -> ExecutionContext:
    exec_context = ExecutionContext()
    exec_context.rule_name = 'test_rule'
    return exec_context
