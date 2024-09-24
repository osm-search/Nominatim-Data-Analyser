from nominatim_data_analyser.core.dynamic_value.variable import Variable
from nominatim_data_analyser.core.dynamic_value.switch import Switch
from pathlib import Path

import nominatim_data_analyser.core.yaml_logic.yaml_loader as yaml_loader
import pytest
import yaml
from nominatim_data_analyser.core.yaml_logic.yaml_loader import load_yaml_rule
from nominatim_data_analyser.core import Pipe

def test_load_yaml_rule(yaml_path) -> None:
    """
        Test the load_yaml_rule() function with a test yaml file.
    """
    yaml_loader.base_rules_path = yaml_path
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

def test_load_wrong_yaml(yaml_path) -> None:
    """
        Test the load_yaml_rule() function with a test yaml file which
        contains wrong syntax. A YAMLError should be raised while loading.
    """
    yaml_loader.base_rules_path = yaml_path
    with pytest.raises(yaml.YAMLError):
        load_yaml_rule('test_load_wrong_yaml')

def test_construct_sub_pipeline(yaml_path) -> None:
    """
        Test that the sub_pipeline_constructor() is well called when
        a specific type !sub-pipeline is present in the YAML file.

        The value should be a Pipe after loading.
    """
    yaml_loader.base_rules_path = yaml_path
    loaded_data = load_yaml_rule('test_construct_sub_pipeline')
    assert isinstance(loaded_data['QUERY']['sub_pipeline'], Pipe)

def test_construct_switch(yaml_path) -> None:
    """
        Test that the switch_constructor() is well called when
        a specific type !switch is present in the YAML file.

        The value should be a Switch after loading.
    """
    yaml_loader.base_rules_path = yaml_path
    loaded_data = load_yaml_rule('test_construct_switch')
    expected_cases = {
        'case1': 'val1',
        'case2': 'val2',
        'case3': 'val3'
    }
    assert isinstance(loaded_data['DUMB_NODE']['value'], Switch)
    assert loaded_data['DUMB_NODE']['value'].expression == 'expression_value'
    assert loaded_data['DUMB_NODE']['value'].cases == expected_cases

def test_construct_variable(yaml_path) -> None:
    """
        Test that the variable_constructor() is well called when
        a specific type !variable is present in the YAML file.

        The value should be a Variable after loading.
    """
    yaml_loader.base_rules_path = yaml_path
    loaded_data = load_yaml_rule('test_construct_variable')
    assert isinstance(loaded_data['DUMB_NODE']['value'], Variable)
    assert loaded_data['DUMB_NODE']['value'].name == 'variable_name'

@pytest.fixture
def yaml_path() -> Path:
    return Path(__file__).parent / 'yaml'
