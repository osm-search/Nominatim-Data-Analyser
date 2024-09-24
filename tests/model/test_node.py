from nominatim_data_analyser.core.model.node import Node
from geojson.feature import Feature


def test_create_from_WKT_string() -> None:
    node = Node.create_from_WKT_string('POINT(10 15)')
    assert node.coordinates[0] == 10 and node.coordinates[1] == 15

def test_to_geojson_feature() -> None:
    """
        Test the to_geojson_feature() method.
        The created feature should have the right geometry, id and properties.
    """
    node = Node.create_from_WKT_string('POINT(10 15)')
    feature: Feature = node.to_geojson_feature(2, {'prop1': 'val1'})
    assert feature['geometry']['type'] == 'Point'
    assert feature['geometry']['coordinates'] == [10, 15]
    assert feature['id'] == 2
    assert feature['properties'] == {'prop1': 'val1'}
