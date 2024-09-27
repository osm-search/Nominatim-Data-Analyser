
from pathlib import Path

import pytest
from nominatim_data_analyser.config import Config
from nominatim_data_analyser.core.core import Core

class TestConfig:

    @pytest.fixture(autouse=True)
    def setup(self, tmp_path) -> None:
        self.rulepath = tmp_path / 'rules'
        cfgfile = tmp_path / 'custom_config.yaml'
        cfgfile.write_text(f"RulesFolderPath: '{self.rulepath}'")

        self.core = Core(config_file=cfgfile)
        self.core.rules_path = Path(__file__).parent / 'rules'

    def test_execute_one(self) -> None:
        """
            Test the execute_one() method. The rule executed only generate a
            dumb geojson file. Therefore we only check if the file is created
            as expected.
        """
        self.core.execute_one('rule1')
        assert (self.rulepath / 'rule1/geojson/rule1.json').is_file()

    def test_execute_all(self) -> None:
        """
            Test the execute_all() method. The two rules only generate a
            dumb geojson file. Therefore we only check if the file are created
            as expected.
        """
        self.core.execute_all()
        assert (self.rulepath / 'rule1/geojson/rule1.json').is_file()
        assert (self.rulepath / 'rule2/geojson/rule2.json').is_file()
