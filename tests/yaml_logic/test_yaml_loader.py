from analyser.core.yaml_logic.yaml_loader import load_yaml_rule 
import analyser.core.yaml_logic.yaml_loader as yaml_loader
from pathlib import Path
import os

def test_load_yaml_rule() -> None:
    """
        Test the load_yaml_rule() function with a test yaml rule file.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    yaml_loader.base_rules_path = Path(f'{dir_path}/../test_data')
    loaded_data = load_yaml_rule('test_yaml_rule')
    assert loaded_data == {
        'QUERY': {
            'type': 'SQLProcessor',
            'query': 'QUERY',
            'out': {
                'DUMB_PIPE': {
                    'type': 'DumbPipe'
                }
            }
        }
    }
