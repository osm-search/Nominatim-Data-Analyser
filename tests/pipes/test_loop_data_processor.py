from nominatim_data_analyser.core.pipes import (LoopDataProcessor,
                                                GeometryConverter,
                                                FillingPipe,
                                                GeoJSONFeatureConverter)
from geojson.feature import Feature


def test_process_one_result(loop_data_processor: LoopDataProcessor,
                            geometry_converter: GeometryConverter,
                            geojson_feature_converter: GeoJSONFeatureConverter) -> None:
    """
        Test the process() method with a pipeline which returns only one result each time.
    """
    geometry_converter.plug_pipe(geojson_feature_converter)

    loop_data_processor.processing_pipeline = geometry_converter
    data = [
        {'geometry_holder': 'POINT(30 155)'},
        {'geometry_holder': 'POINT(4 15)'},
        {'geometry_holder': 'POINT(14 125)'},
        {'geometry_holder': 'POINT(6 1)'}
    ]
    result = loop_data_processor.process(data)
    assert len(result) == 4
    for d in result:
        assert isinstance(d, Feature)


def test_process_multiple_result(loop_data_processor: LoopDataProcessor,
                                 geometry_converter: GeometryConverter,
                                 filling_pipe: FillingPipe,
                                 geojson_feature_converter: GeoJSONFeatureConverter,
                                 monkeypatch) -> None:
    """
        Test the process() method with a pipeline which returns a list of results each time.
        All the results should be added to the results list.
    """
    geometry_converter.plug_pipe(geojson_feature_converter).plug_pipe(filling_pipe)

    # Mock the FillingPipe process() method to return the data 3 times (in a list).
    monkeypatch.setattr('nominatim_data_analyser.core.pipes.filling_pipe.FillingPipe.process',
                        lambda self, data: [data, data, data])

    loop_data_processor.processing_pipeline = geometry_converter
    data = [
        {'geometry_holder': 'POINT(30 155)'},
        {'geometry_holder': 'POINT(4 15)'},
        {'geometry_holder': 'POINT(14 125)'},
        {'geometry_holder': 'POINT(6 1)'}
    ]
    result = loop_data_processor.process(data)

    # 3 results are returned at the end of the pipeline so 4*3=12
    assert len(result) == 12
    for d in result:
        assert isinstance(d, Feature)
