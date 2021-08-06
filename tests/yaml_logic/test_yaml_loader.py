from pathlib import Path

import analyser.core.yaml_logic.yaml_loader as yaml_loader
import pytest
import yaml
from analyser.core.yaml_logic.yaml_loader import load_yaml_rule
from analyser.core import Pipe

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

def test_construct_sub_pipeline() -> None:
    """
        Test that the sub_pipeline_constructor() is well called when
        a specific type !sub-pipeline is present in the YAML file.

        The value should be a Pipe after loading.
    """
    yaml_loader.base_rules_path = Path(__file__).parent
    loaded_data = load_yaml_rule('test_construct_sub_pipeline')
    assert isinstance(loaded_data['QUERY']['sub_pipeline'], Pipe)