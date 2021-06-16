from __future__ import annotations
from analyser.core.pipe import Pipe
from pathlib import Path
import json

class LayerFormatter(Pipe):
    """
        Handles the creation of the layer JSON file.
    """
    def __init__(self, name: str, file_name: str, updates: str) -> None:
        super().__init__()
        self.file_name = file_name
        self.data = dict()
        self.data['id'] = 'SuspectsData'
        self.data['name'] = name
        self.data['doc'] = dict()
        self.data['updates'] = updates
        self.base_folder_path = Path('/srv/nominatim/data-files/layers')

    def add_doc(self, key: str, content: str) -> LayerFormatter:
        """
            Add content under the 'doc' tag of the layer file.
        """
        self.data['doc'][key] = content
        return self

    def process(self, geo_url: str) -> None:
        """
            Create the JSON layer file containing the right data.
            
            It gets the GeoJSON url as data parameter and set it
            inside the layer file.
        """
        self.data['geojson_url'] = geo_url

        folder_path = self.base_folder_path.resolve()
        folder_path.mkdir(parents=True, exist_ok=True)
        full_path = folder_path / Path(self.file_name + '.json')

        with open(full_path, 'w') as json_file:
            json.dump(self.data, json_file)
        
        return None
