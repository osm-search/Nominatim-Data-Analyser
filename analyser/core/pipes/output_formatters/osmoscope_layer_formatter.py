from __future__ import annotations
from analyser.core.model.paths import Paths
from analyser.config.config import Config
from analyser.core import Pipe
from pathlib import Path
import json

class OsmoscopeLayerFormatter(Pipe):
    """
        Handles the creation of the layer JSON file.
    """
    def on_created(self) -> None:   
        self.base_folder_path = Path(f'{Config.values["RulesFolderPath"]}/{self.exec_context.rule_name}/osmoscope-layer')
        self.file_name = self.extract_data('file_name', 'layer')
        self.data_format_url = self.extract_data('data_format_url', required=True)
        self.data['id'] = 'SuspectsData'

    def process(self, paths: Paths) -> None:
        """
            Create the JSON layer file containing the right data.
            
            It gets the GeoJSON url as data parameter and set it
            inside the layer file.
        """
        self.data[self.data_format_url] = paths.web_path
        self.base_folder_path.mkdir(parents=True, exist_ok=True)
        full_path = self.base_folder_path / f'{self.file_name}.json'

        with open(full_path, 'w') as json_file:
            json.dump(self.data, json_file)
        
        file_url = f'{Config.values["WebPrefixPath"]}/{self.exec_context.rule_name}/osmoscope-layer/{self.file_name}.json'
        self.add_layer_to_global_layers_file(file_url)

    def add_layer_to_global_layers_file(self, path: str) -> None:
        """
            Add the newly created layer to the global layers file.
            If the global layers file doesn't exist it is created.
        """
        folder_path = Path(f'{Config.values["RulesFolderPath"]}')
        folder_path.mkdir(parents=True, exist_ok=True)
        full_path = folder_path / 'layers.json'
        full_path.touch(exist_ok=True)

        with open(full_path, 'r') as json_file:
            try:
                data = json.load(json_file)
            except:
                data = {
                    'name': 'Nominatim suspects',
                    'layers': []
                }
        if path not in data['layers']:
            data['layers'].append(path)
        with open(full_path, 'w') as json_file:
            json.dump(data, json_file)
