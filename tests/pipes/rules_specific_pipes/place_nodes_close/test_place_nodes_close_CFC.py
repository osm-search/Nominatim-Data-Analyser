import pytest
from nominatim_data_analyser.core.model import Node
from nominatim_data_analyser.core.pipes.rules_specific_pipes import \
    PlaceNodesCloseCustomFeatureConverter
from nominatim_data_analyser.core.qa_rule import ExecutionContext
from geojson.feature import Feature

def test_process_place_nodes_close_CFC(place_nodes_close_CFC: PlaceNodesCloseCustomFeatureConverter) -> None:
    """
        Test the process() method of the custom pipe PlaceNodesCloseCustomFeatureConverter.
        The method should be procuding a Feature with the expected_properties inside.
    """
    data = {
        'osm_id': 'dumb_osm_id',
        'common_ids': ['CID1', 'CID2', 'CID3'],
        'geometry_holder': Node.create_from_WKT_string('POINT(10 5)')
    }
    expected_properties = {
        'node_id': 'dumb_osm_id',
        'n/@idClose node 1': 'CID1',
        'n/@idClose node 2': 'CID2',
        'n/@idClose node 3': 'CID3'
    }
    result = place_nodes_close_CFC.process(data)
    assert isinstance(result, Feature)
    assert result['properties'] == expected_properties

@pytest.fixture
def place_nodes_close_CFC(execution_context: ExecutionContext) -> PlaceNodesCloseCustomFeatureConverter:
    return PlaceNodesCloseCustomFeatureConverter({}, execution_context)
