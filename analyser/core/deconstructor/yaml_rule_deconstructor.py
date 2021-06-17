import yaml
import logging
from pathlib import Path

LOG = logging.getLogger()

class YAMLRuleDeconstructor():
    """
        Deconstruct a YAML rule file.
    """
    def __init__(self, file_name: str) -> None:
        self.loaded_data = self._load_yaml(file_name)

    def get_next_sql_fetcher(self) -> dict:
        """
            Returns the next sql fetcher from the YAML specification
            if there is any one left.
            It gets removed from the loaded data as soon as it is returned.
        """
        if 'SQLFetchers' in self.loaded_data and self.loaded_data['SQLFetchers']:
            for key in self.loaded_data['SQLFetchers']:
                return self.loaded_data['SQLFetchers'].pop(key)
        return None

    def get_osmoscope_output(self) -> dict:
        """
            Returns the osmoscope output specification if any.
        """
        if 'Outputs' in self.loaded_data and 'omoscope' in self.loaded_data['Outputs']:
            return self.loaded_data['Outputs']['omoscope']
        return None

    def _load_yaml(self, file_name: str) -> dict:
        path = Path(Path('analyser/rules_specifications') / Path(file_name + '.yaml')).resolve()
        with open(str(path), 'r') as file:
            try:
                return yaml.safe_load(file)
            except yaml.YAMLError as exc:
                LOG.error('Error while loading the YAML rule file %s: %s',
                          file_name, exc)