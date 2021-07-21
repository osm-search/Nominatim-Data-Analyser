from __future__ import annotations
from analyser.core.model.paths import Paths
from typing import List
from geojson.feature import Feature
from analyser.core import Pipe
from pathlib import Path
from geojson import FeatureCollection, dump

FULL_PATH_PREFIX = 'https://gsoc2021-qa.nominatim.org/QA-data/geojson'

class GeoJSONFormatter(Pipe):
    """
        Handles the creation of the GeoJSON file.
    """
    def on_created(self) -> None:
        self.base_folder_path = Path('/srv/nominatim/data-files/geojson')
        self.file_name = self.extract_data('file_name')

    def process(self, features: List[Feature]) -> Paths:
        """
            Create the FeatureCollection and dump it to
            a new GeoJSON file.
        """
        feature_collection = FeatureCollection(features)
        folder_path = Path(self.base_folder_path).resolve()
        folder_path.mkdir(parents=True, exist_ok=True)
        full_path = folder_path / Path(self.file_name + '.json')

        with open(full_path, 'w') as file:
            dump(feature_collection, file)

        web_path = FULL_PATH_PREFIX + '/' + self.file_name + '.json'
        return Paths(web_path, str(full_path.resolve()))
