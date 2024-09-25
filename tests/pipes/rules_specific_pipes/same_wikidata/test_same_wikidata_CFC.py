import pytest
from nominatim_data_analyser.core.pipes.rules_specific_pipes import \
    SameWikiDataFeatureConverter
from nominatim_data_analyser.core.qa_rule import ExecutionContext


def test_same_wikidata_CFC(same_wikidata_CFC: SameWikiDataFeatureConverter) -> None:
    """
        Test the process() method of the custom pipe SameWikiDataFeatureConverter.
        The method should be procuding a List of features with the right values 
        matching the expected_results.
    """
    data = [
        {
            'wikidata': 'dumb_wikidata1',
            'ids': ['ID1', 'ID2', 'ID3'],
            'centroids': ['POINT(5 2)', 'POINT(8 3)', None]
        },
        {
            'wikidata': 'dumb_wikidata2',
            'ids': ['ID4', 'ID5'],
            'centroids': ['POINT(8 10)', 'POINT(80 30)']
        }
    ]
    expected_results = [
        {
            "geometry": {"coordinates": [5.0, 2.0], "type": "Point"}, 
            "id": 0, 
            "properties": {"n/@idNode in common 1": "ID2", "n/@idNode in common 2": "ID3", "node_id": "ID1", "wikidata in common": "dumb_wikidata1"}, 
            "type": "Feature"
        }, 
        {
            "geometry": {"coordinates": [8.0, 3.0], "type": "Point"}, 
            "id": 1, 
            "properties": {"n/@idNode in common 1": "ID1", "n/@idNode in common 2": "ID3", "node_id": "ID2", "wikidata in common": "dumb_wikidata1"}, 
            "type": "Feature"
        }, 
        {
            "geometry": {"coordinates": [8.0, 10.0], "type": "Point"}, 
            "id": 2, 
            "properties": {"n/@idNode in common 1": "ID5", "node_id": "ID4", "wikidata in common": "dumb_wikidata2"}, 
            "type": "Feature"}, 
        {
            "geometry": {"coordinates": [80.0, 30.0], "type": "Point"}, 
            "id": 3, 
            "properties": {"n/@idNode in common 1": "ID4", "node_id": "ID5", "wikidata in common": "dumb_wikidata2"}, 
            "type": "Feature"
        }
    ]
    results = same_wikidata_CFC.process(data)
    assert results == expected_results

@pytest.fixture
def same_wikidata_CFC(execution_context: ExecutionContext) -> SameWikiDataFeatureConverter:
    return SameWikiDataFeatureConverter({}, execution_context)
