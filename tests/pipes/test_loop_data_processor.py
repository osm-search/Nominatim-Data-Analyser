from analyser.core.pipes.data_processing import LoopDataProcessor
from analyser.core.pipes.data_processing.geometry_converter import \
    GeometryConverter
from analyser.core.pipes.filling_pipe import FillingPipe
from analyser.core.pipes.output_formatters.geojson_feature_converter import \
    GeoJSONFeatureConverter
from geojson.feature import Feature


def test_process_one_data_not_none(loop_data_processor: LoopDataProcessor,
                                   geometry_converter: GeometryConverter,
                                   geojson_feature_converter: GeoJSONFeatureConverter) -> None:
    """
        Test the process_one_data() method with a sub-pipeline which should not return None.
    """
    geometry_converter.plug_pipe(geojson_feature_converter)
    loop_data_processor.processing_pipeline = geometry_converter
    result = loop_data_processor.process_one_data({'geometry_holder': 'POINT(10 15)'})
    assert isinstance(result, Feature)

def test_process_one_data_none(loop_data_processor: LoopDataProcessor,
                               geometry_converter: GeometryConverter,
                               filling_pipe: FillingPipe,
                               geojson_feature_converter: GeoJSONFeatureConverter,
                               monkeypatch) -> None:
    """
        Test the process_one_data() method with 
        a pipe in the middle of the sub-pipeline which returns None.
        Therefore, the result should be None.
    """
    geometry_converter.plug_pipe(filling_pipe).plug_pipe(geojson_feature_converter)

    #Mock the FillingPipe process() method to return None.
    monkeypatch.setattr('analyser.core.pipes.filling_pipe.FillingPipe.process',
                        lambda self, data: None)

    loop_data_processor.processing_pipeline = geometry_converter
    result = loop_data_processor.process_one_data({'geometry_holder': 'POINT(10 15)'})
    assert not result

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

    #Mock the FillingPipe process() method to return the data 3 times (in a list).
    monkeypatch.setattr('analyser.core.pipes.filling_pipe.FillingPipe.process',
                        lambda self, data: [data, data, data])

    loop_data_processor.processing_pipeline = geometry_converter
    data = [
        {'geometry_holder': 'POINT(30 155)'},
        {'geometry_holder': 'POINT(4 15)'},
        {'geometry_holder': 'POINT(14 125)'},
        {'geometry_holder': 'POINT(6 1)'}
    ]
    result = loop_data_processor.process(data)

    #3 results are returned at the end of the pipeline so 4*3=12
    assert len(result) == 12
    for d in result:
        assert isinstance(d, Feature)
