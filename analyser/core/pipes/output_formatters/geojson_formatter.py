from __future__ import annotations
from analyser.config import Config
from analyser.core.model.paths import Paths
from typing import List
from geojson.feature import Feature
from analyser.core import Pipe
from pathlib import Path
from geojson import FeatureCollection, dump

class GeoJSONFormatter(Pipe):
    """
        Handles the creation of the GeoJSON file.
    """
    def on_created(self) -> None:
        self.base_folder_path = Path(f'{Config.values["RulesFolderPath"]}/{self.exec_context.rule_name}/geojson')
        #Take the rule's name as default file name.
        self.file_name = self.extract_data('file_name', self.exec_context.rule_name)

    def process(self, features: List[Feature]) -> Paths:
        """
            Create the FeatureCollection and dump it to
            a new GeoJSON file.
        """
        feature_collection = FeatureCollection(features)
        self.base_folder_path.mkdir(parents=True, exist_ok=True)
        full_path = self.base_folder_path / f'{self.file_name}.json'

        with open(full_path, 'w') as file:
            dump(feature_collection, file)

        web_path = f'{Config.values["WebPrefixPath"]}/{self.exec_context.rule_name}/geojson/{self.file_name}.json'
        return Paths(web_path, str(full_path.resolve()))
