from analyser.core.pipes.output_formatters import GeoJSONFeatureConverter
from analyser.core.model import Node
from geojson.feature import Feature

def test_on_created_geojson_feature_converter(geojson_feature_converter: GeoJSONFeatureConverter) -> None:
    """
        Test the on_created() method of the GeoJSONFeatureConverter.
    """
    geojson_feature_converter.properties_pattern = None
    geojson_feature_converter.data['properties'] = {'prop1': 'val1'}
    geojson_feature_converter.on_created()
    assert geojson_feature_converter.properties_pattern == {'prop1': 'val1'}

def test_process_geojson_feature_converter(geojson_feature_converter: GeoJSONFeatureConverter) -> None:
    """
        Test the process() method of the GeoJSONFeatureConverter.
    """
    data = {
        'geometry_holder': Node.create_from_WKT_string('POINT(10 15)')
    }
    feature: Feature = geojson_feature_converter.process(data)
    assert feature['geometry']['type'] == 'Point'
    assert feature['geometry']['coordinates'] == [10, 15]
    assert feature['properties'] == {'prop1': 'val1', 'prop2': 'val2'}