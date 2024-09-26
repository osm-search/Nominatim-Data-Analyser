from pathlib import Path
import json

import psycopg

from ....config import Config
from ... import Pipe

class OsmoscopeLayerFormatter(Pipe):
    """
        Handles the creation of the layer JSON file.
    """
    def on_created(self) -> None:
        self.base_folder_path = Path(f'{Config.values["RulesFolderPath"]}/{self.exec_context.rule_name}/osmoscope-layer')
        self.file_name = self.extract_data('file_name', 'layer')
        self.data_format_url = self.extract_data('data_format_url', required=True)
        self.data['id'] = self.extract_data('id', default=self.exec_context.rule_name)

    def process(self, data_source_path: str) -> None:
        """
            Create the JSON layer file containing the right data.

            It gets the GeoJSON url as data parameter and set it
            inside the layer file.
        """
        self.add_last_update_date_layer_info()
        self.data[self.data_format_url] = data_source_path
        self.base_folder_path.mkdir(parents=True, exist_ok=True)
        full_path = self.base_folder_path / f'{self.file_name}.json'

        with open(full_path, 'w') as json_file:
            json.dump(self.data, json_file)

        file_url = f'{Config.values["WebPrefixPath"]}/{self.exec_context.rule_name}/osmoscope-layer/{self.file_name}.json'
        self.add_layer_to_global_layers_file(file_url)

    def add_last_update_date_layer_info(self) -> None:
        """
            Add a "last_update" field to the layer information.
            This field contains the date of the last database update.
            The date is extracted from the lastimportdate table of the database.
        """
        with psycopg.connect(Config.values['Dsn']) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT to_char(lastimportdate at time zone 'UTC', "
                            "               'YYYY-MM-DD HH24:MI:SS UTC') FROM import_status")
                last_update_date = cur.fetchone()
        if last_update_date:
            if 'doc' not in self.data:
                self.data['doc'] = {}
            self.data['doc']['last_update'] = last_update_date[0]

    def add_layer_to_global_layers_file(self, path: str) -> None:
        """
            Add the newly created layer to the global layers file.
            If the global layers file doesn't exist it is created.
        """
        folder_path = Path(f'{Config.values["RulesFolderPath"]}')
        folder_path.mkdir(parents=True, exist_ok=True)
        # Check if the folder_path has a parent because /layers.json will require sudo permissions.
        full_path = folder_path / 'layers.json' if len(folder_path.parents) > 0 else Path('layers.json')
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
