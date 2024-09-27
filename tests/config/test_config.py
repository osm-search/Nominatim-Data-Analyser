import pytest
import yaml

from nominatim_data_analyser.config import Config, load_config

def test_load_default_config() -> None:
    """
        Test the load_config() method. The default config should be
        returned because no config.yaml file is present in the
        default_config folder used as the config_folder_path.
    """
    load_config(None)
    assert Config.values['Dsn'] == 'dbname=nominatim'
    assert Config.values['RulesFolderPath'] == 'qa-data'

def test_load_custom_config(tmp_path) -> None:
    """
        Test the load_config() method. The custom config should be
        returned because one config.yaml file is present in the
        custom_config folder used as the config_folder_path.
    """
    cfgfile = tmp_path / 'myconfig.yaml'
    cfgfile.write_text("Dsn: 'custom_dsn'")

    load_config(cfgfile)

    assert Config.values['Dsn'] == 'custom_dsn'
    assert Config.values['RulesFolderPath'] == 'qa-data'

def test_load_broken_config(tmp_path) -> None:
    """
        Test the load_config() method. A YAMLError exception should
        be raised as the config file has a wrong syntax.
    """
    cfgfile = tmp_path / 'myconfig.yaml'
    cfgfile.write_text(">>>>>>>>Dsn: 'custom_dsn'")

    with pytest.raises(yaml.YAMLError):
        load_config(cfgfile)
