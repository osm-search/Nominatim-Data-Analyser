from __future__ import annotations
from typing import List
from geojson.feature import Feature
from analyser.core.pipe import Pipe
from pathlib import Path
from geojson import FeatureCollection, dump
import typing

if typing.TYPE_CHECKING:
    from analyser.core.qa_rule import ExecutionContext

FULL_PATH_PREFIX = 'https://QA-data/geojson'

class GeoJSONFormatter(Pipe):
    """
        Handles the creation of the GeoJSON file.
    """
    def __init__(self, filename: str, exec_context: ExecutionContext) -> None:
        super().__init__(exec_context)
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
    
    @staticmethod
    def create_from_node_data(data: dict, exec_context: ExecutionContext) -> GeoJSONFormatter:
        """
            Assembles the pipe with the given node data.
        """
        return GeoJSONFormatter(data['file_name'], exec_context)
