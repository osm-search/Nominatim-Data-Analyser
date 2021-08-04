from analyser.core.pipes.output_formatters import GeoJSONFormatter
from analyser.core.model import Paths
from geojson import Feature, Point, FeatureCollection, loads
from analyser.config.config import Config

def test_process_geojson_formatter(config: Config,
                                   geojson_formatter: GeoJSONFormatter, 
                                   tmp_path) -> None:
    """
        Test the process() method of the GeoJSONFormatter.
        A temporary folder is used as the base folder.

        the 'test_folder' doesn't exist initially and should be well
        created by the method.
    """
    config.values['WebPrefixPath'] = 'test_prefix_path'
    geojson_formatter.file_name = 'test_file'
    geojson_formatter.base_folder_path = tmp_path / 'test_folder'

    features = [
        Feature(geometry=Point((5, 2))),
        Feature(geometry=Point((4, 1))),
        Feature(geometry=Point((10, 20)))
    ]

    result: Paths = geojson_formatter.process(features)
    assert result.local_path == str((tmp_path / 'test_folder' / 'test_file.json').resolve())
    assert result.web_path == 'test_prefix_path/test_rule/geojson/test_file.json'

    #Verify the content of the geojson created
    with open(result.local_path, 'r') as file:
        assert loads(file.read()) == FeatureCollection(features)