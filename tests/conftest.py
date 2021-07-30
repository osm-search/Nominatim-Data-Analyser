from analyser.core.pipes.data_fetching.sql_processor import SQLProcessor
from analyser.core.pipes.output_formatters import GeoJSONFormatter
from analyser.core.pipes.output_formatters import GeoJSONFeatureConverter
from analyser.core.pipes.data_processing import GeometryConverter
from analyser.core.qa_rule import ExecutionContext
from analyser.core.pipes import FillingPipe
import pytest

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
    return GeoJSONFeatureConverter({}, execution_context)

@pytest.fixture
def geojson_formatter(execution_context) -> GeoJSONFormatter:
    return GeoJSONFormatter({}, execution_context)

@pytest.fixture
def execution_context() -> ExecutionContext:
    exec_context = ExecutionContext()
    exec_context.rule_name = 'test_rule'
    return exec_context