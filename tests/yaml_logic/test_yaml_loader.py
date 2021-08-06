import os
from pathlib import Path

import analyser.core.yaml_logic.yaml_loader as yaml_loader
import pytest
import yaml
from analyser.core.yaml_logic.yaml_loader import load_yaml_rule


def test_load_yaml_rule() -> None:
    """
        Test the load_yaml_rule() function with a test yaml file.
    """
    yaml_loader.base_rules_path = Path(__file__).parent
    loaded_data = load_yaml_rule('test_load_yaml')
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

def test_load_wrong_yaml() -> None:
    """
        Test the load_yaml_rule() function with a test yaml file which
        contains wrong syntax. A YAMLError should be raised while loading.
    """
    yaml_loader.base_rules_path = Path(__file__).parent
    with pytest.raises(yaml.YAMLError):
        load_yaml_rule('test_load_wrong_yaml')