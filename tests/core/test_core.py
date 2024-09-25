
from pathlib import Path

import pytest
from nominatim_data_analyser.config.config import Config
from nominatim_data_analyser.core.core import Core

rules_path = Path(__file__).parent / 'rules'

def test_execute_one(core: Core, tmp_path, monkeypatch) -> None:
    """
        Test the execute_one() method. The rule executed only generate a
        dumb geojson file. Therefore we only check if the file is created
        as expected.
    """
    setup_mock(tmp_path, monkeypatch)
    core.execute_one('rule1')
    assert (tmp_path / 'rule1/geojson/rule1.json').is_file()

def test_execute_all(core: Core, monkeypatch, tmp_path) -> None:
    """
        Test the execute_all() method. The two rules only generate a
        dumb geojson file. Therefore we only check if the file are created
        as expected.
    """
    setup_mock(tmp_path, monkeypatch)
    core.rules_path = rules_path
    core.execute_all()
    assert (tmp_path / 'rule1/geojson/rule1.json').is_file()
    assert (tmp_path / 'rule2/geojson/rule2.json').is_file()

def setup_mock(tmp_path, monkeypatch) -> None:
    """
        Mock the yaml_loader base_rule_path to match the
        local test rules folder.
        Set the RulesFolderPath to the temporary folder of the
        test for the creation of output files.
    """
    monkeypatch.setattr('nominatim_data_analyser.core.yaml_logic.yaml_loader.base_rules_path',
                        rules_path)
    Config.values['RulesFolderPath'] = tmp_path

@pytest.fixture
def core() -> Core:
    return Core()
