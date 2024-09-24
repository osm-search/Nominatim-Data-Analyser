from nominatim_data_analyser.core.pipes.data_processing import GeometryConverter

def test_on_created_geometry_converter(geometry_converter: GeometryConverter) -> None:
    """
        Test the on_created() method of the GeometryConverter.
    """
    geometry_converter.geometry_type = None
    geometry_converter.data['geometry_type'] = 'Node'
    geometry_converter.on_created()
    assert geometry_converter.geometry_type == 'Node'

def test_process_geometry_converter(geometry_converter: GeometryConverter) -> None:
    """
        Test the process() method of the GeometryConverter.
    """
    data_result = geometry_converter.process({'geometry_holder': 'POINT(10 15)'})
    assert data_result['geometry_holder'].coordinates[0] == 10 and data_result['geometry_holder'].coordinates[1] == 15

def test_process_geometry_converter_none_geometry_holder(geometry_converter: GeometryConverter) -> None:
    """
        Test the process() method of the GeometryConverter with one data containing a None value for the geometry_holder.
    """
    data_result = geometry_converter.process({'geometry_holder': None})
    assert data_result is None
