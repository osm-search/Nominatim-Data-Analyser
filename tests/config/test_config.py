
from analyser.config import Config
from pathlib import Path
import pytest
import yaml

def test_load_default_config(config: Config) -> None:
    """
        Test the load_config() method. The default config should be
        returned because no config.yaml file is present in the
        default_config folder used as the config_folder_path.
    """
    config.load_config(Path(__file__).parent / 'default_config')
    assert config.values == {'Dsn': 'default_dsn'}

def test_load_custom_config(config: Config) -> None:
    """
        Test the load_config() method. The custom config should be
        returned because one config.yaml file is present in the
        custom_config folder used as the config_folder_path.
    """
    config.load_config(Path(__file__).parent / 'custom_config')
    assert config.values == {'Dsn': 'custom_dsn'}

def test_load_broken_config(config: Config) -> None:
    """
        Test the load_config() method. A YAMLError exception should
        be raised as the config file has a wrong syntax.
    """
    with pytest.raises(yaml.YAMLError):
        config.load_config(Path(__file__).parent / 'broken_config')