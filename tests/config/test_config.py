
from nominatim_data_analyser.config import Config, load_config
from pathlib import Path
import pytest
import yaml

def test_load_default_config() -> None:
    """
        Test the load_config() method. The default config should be
        returned because no config.yaml file is present in the
        default_config folder used as the config_folder_path.
    """
    load_config(None)
    assert Config.values['Dsn'] == 'dbname=nominatim'

def test_load_custom_config() -> None:
    """
        Test the load_config() method. The custom config should be
        returned because one config.yaml file is present in the
        custom_config folder used as the config_folder_path.
    """
    load_config(Path(__file__).parent / 'custom_config' / 'config.yaml')
    assert Config.values == {'Dsn': 'custom_dsn'}

def test_load_broken_config() -> None:
    """
        Test the load_config() method. A YAMLError exception should
        be raised as the config file has a wrong syntax.
    """
    with pytest.raises(yaml.YAMLError):
        load_config(Path(__file__).parent / 'broken_config' / 'default.yaml')
