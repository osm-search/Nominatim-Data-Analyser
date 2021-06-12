from __future__ import annotations
import json
from pathlib import Path

class LayerFormatter():
    """
        Handles the creation of the layer JSON file.
    """
    def __init__(self, layername: str, updates: str) -> None:
        self.layername = layername
        self.data = dict()
        self.data['id'] = 'SuspectsData'
        self.data['name'] = layername
        self.data['doc'] = dict()
        self.data['updates'] = updates
        self.base_folder_path = Path('/srv/nominatim/data-files/layers')

    def add_doc(self, key: str, content: str) -> LayerFormatter:
        """
            Add content under the 'doc' tag of the layer file.
        """
        self.data['doc'][key] = content
        return self

    def set_geojson_url(self, url: str) -> LayerFormatter:
        """
            Set the given url to the geojson_url field of
            the layer file.
        """
        self.data['geojson_url'] = url
        return self

    def process(self, target: str = '') -> None:
        """
            Create the JSON layer file containing the right data.
            The layer file is created in the given target folder.
        """
        folder_path = Path(self.base_folder_path / Path(target)).resolve()
        folder_path.mkdir(parents=True, exist_ok=True)
        full_path = folder_path / Path(self.layername + '.json')

        with open(full_path, 'w') as json_file:
            json.dump(self.data, json_file)
