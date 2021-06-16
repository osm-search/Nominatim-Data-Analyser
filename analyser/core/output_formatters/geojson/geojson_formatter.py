from typing import List
from geojson.feature import Feature
from analyser.core.pipe import Pipe
from pathlib import Path
from geojson import FeatureCollection, dump

FULL_PATH_PREFIX = 'https://QA-data/geojson'

class GeoJSONFormatter(Pipe):
    """
        Handles the creation of the GeoJSON file.
    """
    def __init__(self, filename: str) -> None:
        super().__init__()
        self.base_folder_path = Path('/srv/nominatim/data-files/geojson')
        self.sub_folder = ''
        self.file_name = filename

    def process(self, features: List[Feature]) -> str:
        """
            Create the FeatureCollection and dump it to
            a new GeoJSON file.
        """
        feature_collection = FeatureCollection(features)
        folder_path = Path(self.base_folder_path / Path(self.sub_folder)).resolve()
        folder_path.mkdir(parents=True, exist_ok=True)
        full_path = folder_path / Path(self.file_name + '.json')

        with open(full_path, 'w') as file:
            dump(feature_collection, file)

        return str(Path(FULL_PATH_PREFIX / Path(self.sub_folder) / Path(self.file_name + '.json')))
