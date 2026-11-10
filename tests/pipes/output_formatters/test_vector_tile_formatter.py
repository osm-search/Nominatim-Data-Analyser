from nominatim_data_analyser.core.pipes import VectorTileFormatter
from nominatim_data_analyser.config import Config
from geojson import Feature, Point, FeatureCollection, loads


def test_process_vector_tile_formatter(vector_tile_formatter: VectorTileFormatter,
                                       config: Config,
                                       tmp_path,
                                       monkeypatch) -> None:
    """
        test the process() method.
        A temporary folder is used as the base folder.

        the 'test_folder' doesn't exist initially and should be well
        created by the method.

        The call to Tippecanoe is mocked to nothing because we dont want
        to test Tippecanoe.
    """
    config.values['WebPrefixPath'] = 'test_prefix_path'
    vector_tile_formatter.base_folder_path = tmp_path / 'test_folder'
    vector_tile_formatter.geojson_formatter.base_folder_path = tmp_path / 'geojson'

    features = [
        Feature(geometry=Point((5, 2))),
        Feature(geometry=Point((4, 1))),
        Feature(geometry=Point((10, 20)))
    ]

    # Mock the call to Tippecanoe
    monkeypatch.setattr('nominatim_data_analyser.core.pipes.output_formatters.vector_tile_formatter.VectorTileFormatter.call_tippecanoe',  # noqa: E501
                        lambda self, output_dir, feature_collection: None)

    web_path = vector_tile_formatter.process(features)
    assert web_path == 'test_prefix_path/test_rule/vector-tiles/{z}/{x}/{y}.pbf'

    # The features are also written to a GeoJSON file.
    with open(tmp_path/'geojson/test_rule.json', 'r') as file:
        assert loads(file.read()) == FeatureCollection(features)
