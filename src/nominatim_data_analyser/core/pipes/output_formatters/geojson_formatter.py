from typing import Any
from ....config import Config
from geojson.feature import Feature
from ....core import Pipe
from pathlib import Path
from geojson import FeatureCollection, dump
import gzip


class GeoJSONFormatter(Pipe):
    """
        Handles the creation of the GeoJSON file.
    """
    def on_created(self) -> None:
        self.base_folder_path = Path(Config.values["RulesFolderPath"],
                                     self.exec_context.rule_name,
                                     'geojson')
        # Take the rule's name as default file name.
        self.file_name = self.extract_data('file_name', self.exec_context.rule_name)
        # Write a gzip-compressed .json.gz file instead of plain .json.
        self.compress: bool = self.extract_data('compress', default=False)

    def process(self, features: Any) -> str:
        """
            Create the FeatureCollection and dump it to
            a new GeoJSON file.
        """
        if isinstance(features, list):
            feature_collection = FeatureCollection([f for f in features if isinstance(f, Feature)])
        else:
            feature_collection = FeatureCollection([])

        self.base_folder_path.mkdir(parents=True, exist_ok=True)
        file_name = f'{self.file_name}.json.gz' if self.compress else f'{self.file_name}.json'
        full_path = self.base_folder_path / file_name

        with gzip.open(full_path, 'wt') if self.compress else open(full_path, 'w') as file:
            dump(feature_collection, file)

        return f"{Config.values['WebPrefixPath']}/{self.exec_context.rule_name}"\
               f"/geojson/{file_name}"
