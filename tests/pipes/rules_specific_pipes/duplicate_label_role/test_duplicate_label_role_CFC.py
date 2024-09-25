import pytest
from nominatim_data_analyser.core.model import Node
from nominatim_data_analyser.core.pipes.rules_specific_pipes import \
    DuplicateLabelRoleCustomFeatureConverter
from nominatim_data_analyser.core.qa_rule import ExecutionContext
from geojson.feature import Feature


def test_process_duplicate_label_role_CFC(duplicate_label_role_CFC: DuplicateLabelRoleCustomFeatureConverter) -> None:
    """
        Test the process() method of the custom pipe DuplicateLabelRoleCustomFeatureConverter.
        The method should be procuding a Feature with the expected_properties inside.
    """
    data = {
        'osm_id': 'dumb_osm_id',
        'members': ['w8125151','outer','w249285853','inner',
                    'w25151','label','w24953','inner',
                    'w8121','label','w5853','label'],
        'geometry_holder': Node.create_from_WKT_string('POINT(10 5)')
    }
    expected_properties = {
        'relation_id': 'dumb_osm_id',
        'w/@idLabel 1': '25151',
        'w/@idLabel 2': '8121',
        'w/@idLabel 3': '5853'
    }
    result = duplicate_label_role_CFC.process(data)
    assert isinstance(result, Feature)
    assert result['properties'] == expected_properties

@pytest.fixture
def duplicate_label_role_CFC(execution_context: ExecutionContext) -> DuplicateLabelRoleCustomFeatureConverter:
    return DuplicateLabelRoleCustomFeatureConverter({}, execution_context)
