import logging
from pathlib import Path

from .yaml_logic.yaml_loader import load_yaml_rule
from .assembler.pipeline_assembler import PipelineAssembler
from ..timer import Timer
from ..config import load_config

LOG = logging.getLogger()

class Core():
    """
        Core of the analyser used to execute rules.
    """
    def __init__(self, config_file: str | Path | None) -> None:
        load_config(None if config_file is None else Path(config_file))
        self.rules_path = Path(__file__, '..', '..', 'rules_specifications').resolve()

    def execute_all(self, filter: list[str] | None = None) -> None:
        """
            Execute each QA rules.

            If a filter is given as parameter, the rules inside this
            filter wont be executed.
        """
        for rule_file in self.rules_path.glob('*.yaml'):
            if not filter or rule_file.stem not in filter:
                self._execute(rule_file)

    def execute_one(self, name: str) -> None:
        """
            Execute one QA rule based on its YAML file name.
        """
        self._execute(self.rules_path / f"{name}.yaml")

    def _execute(self, rule_file: Path) -> None:
        timer = Timer(f'<{rule_file.stem}> The whole rule')
        loaded_yaml = load_yaml_rule(rule_file)
        PipelineAssembler(loaded_yaml, rule_file.stem).assemble().process_and_next()
        LOG.info(timer.elapsed_str)
