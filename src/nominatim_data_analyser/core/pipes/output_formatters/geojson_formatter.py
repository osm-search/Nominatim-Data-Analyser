from __future__ import annotations
from ....config import Config
from typing import List
from geojson.feature import Feature
from ....core import Pipe
from pathlib import Path
from geojson import FeatureCollection, dump

class GeoJSONFormatter(Pipe):
    """
        Handles the creation of the GeoJSON file.
    """
    def on_created(self) -> None:
        self.base_folder_path = Path(f'{Config.values["RulesFolderPath"]}/{self.exec_context.rule_name}/geojson')
        # Take the rule's name as default file name.
        self.file_name = self.extract_data('file_name', self.exec_context.rule_name)

    def process(self, features: List[Feature]) -> str:
        """
            Create the FeatureCollection and dump it to
            a new GeoJSON file.
        """

        # tippecanoe (using sqlite as datastore) converts Null to 0.
        # https://github.com/mapbox/tippecanoe/issues/811
        # Thus loop through all features and remove any properties having Null values.
        if features is not None:
            for feature in features:
                feature['properties'] = {k: v for k, v in feature['properties'].items() if v is not None}

        feature_collection = FeatureCollection(features)
        self.base_folder_path.mkdir(parents=True, exist_ok=True)
        full_path = self.base_folder_path / f'{self.file_name}.json'

        with open(full_path, 'w') as file:
            dump(feature_collection, file)

        web_path = f'{Config.values["WebPrefixPath"]}/{self.exec_context.rule_name}/geojson/{self.file_name}.json'
        return web_path
