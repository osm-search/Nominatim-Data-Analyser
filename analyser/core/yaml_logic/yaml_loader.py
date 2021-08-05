from pathlib import Path
from analyser.logger.logger import LOG
import yaml

base_rules_path = Path('analyser/rules_specifications')

def load_yaml_rule(file_name: str) -> dict:
    """
        Load the YAML specification file.
    """
    path = Path(base_rules_path / Path(file_name + '.yaml')).resolve()
    with open(str(path), 'r') as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as exc:
            LOG.error('Error while loading the YAML rule file %s: %s',
                        file_name, exc)
            raise