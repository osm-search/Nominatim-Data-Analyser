from analyser.core.pipes.data_fetching.sql_processor import SQLProcessor
from analyser.core.pipes.output_formatters import GeoJSONFeatureConverter
from analyser.core.pipes.data_processing import GeometryConverter
from analyser.core.pipes.filling_pipe import FillingPipe
from analyser.core.assembler import PipelineAssembler
from analyser.core.pipe import Pipe
import pytest

def test_on_new_node(pipeline_assembler: PipelineAssembler, filling_pipe: Pipe) -> None:
    """
        Test the on_new_node() method.
        The given node is not of type 'ROOT_NODE' so it should be
        created, plugged to the top pipe of the nodes history and added
        on the top of the nodes history deque.
    """
    node = {
        'type': 'GeometryConverter',
        'geometry_type': 'Node'
    }
    #Add a FillingPipe as first pipe to the nodes history.
    first_pipe = filling_pipe
    pipeline_assembler.nodes_history.append(first_pipe)
    pipeline_assembler.on_new_node(node)
    new_top_node = pipeline_assembler.nodes_history.pop()
    #Check that the new top node is the right type.
    assert isinstance(new_top_node, GeometryConverter)
    #Check that the new top node is the one plugged to the first_pipe.
    assert first_pipe.next_pipes.pop() == new_top_node

def test_on_new_node_root(pipeline_assembler: PipelineAssembler) -> None:
    """
        Test the on_new_node() method.
        The given node is of type 'ROOT_NODE', hence a
        FillingPipe should be added to the nodes history as the first pipe.
    """
    node = {
        'type': 'ROOT_NODE'
    }
    assert len(pipeline_assembler.nodes_history) == 0
    pipeline_assembler.on_new_node(node)
    assert isinstance(pipeline_assembler.nodes_history.pop(), FillingPipe)

def test_on_backtrack(pipeline_assembler: PipelineAssembler,
                      filling_pipe: FillingPipe,
                      geometry_converter: GeometryConverter,
                      geojson_feature_converter: GeoJSONFeatureConverter,
                      sql_processor: SQLProcessor) -> None:
    """
        Test the on_backtrack() method.
        By applying a batrack of 2 the two last
        pipes of the nodes_history should be removed.
    """
    pipeline_assembler.nodes_history.extend([
        filling_pipe,
        geometry_converter,
        geojson_feature_converter,
        sql_processor
    ])
    pipeline_assembler.on_backtrack(2)
    assert pipeline_assembler.nodes_history.pop() == geometry_converter

def test_assemble() -> None:
    """
        Test the assemble() method.
        A basic pipeline specification is given, only the execution is tested.
    """
    pipeline_specification = {
        'QUERY': {
            'type': 'SQLProcessor',
            'query': 'SELECT 1 FROM foo'
        }
    }
    pipeline_assembler = PipelineAssembler(pipeline_specification, 'test_rule')
    assert isinstance(pipeline_assembler.assemble(), FillingPipe)

@pytest.fixture
def pipeline_assembler() -> PipelineAssembler:
    return PipelineAssembler({}, 'test_rule')