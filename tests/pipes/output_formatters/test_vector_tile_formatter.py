from analyser.core.pipes import VectorTileFormatter
from analyser.config import Config
from geojson import Feature, Point

def test_process_vector_tile_formatter(vector_tile_formatter: VectorTileFormatter,
                                       config: Config,
                                       tmp_path) -> None:
    """
        test the process() method.
        A temporary folder is used as the base folder.

        the 'test_folder' doesn't exist initially and should be well
        created by the method.

        The call to Tippecanoe is tested indirectly.
    """
    config.values['WebPrefixPath'] = 'test_prefix_path'
    vector_tile_formatter.base_folder_path = tmp_path / 'test_folder'

    features = [
        Feature(geometry=Point((5, 2))),
        Feature(geometry=Point((4, 1))),
        Feature(geometry=Point((10, 20)))
    ]

    paths = vector_tile_formatter.process(features)
    assert paths.web_path == 'test_prefix_path/test_rule/vector-tiles/{z}/{x}/{y}.pbf'
    assert paths.local_path == str((tmp_path / 'test_folder').resolve())