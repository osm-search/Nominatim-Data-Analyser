from .yaml_logic.yaml_loader import load_yaml_rule
from .assembler.pipeline_assembler import PipelineAssembler
from ..logger.logger import LOG
from ..logger.timer import Timer
from ..config import Config
from pathlib import Path
from typing import Dict

class Core():
    """
        Core of the analyser used to execute rules.
    """
    def __init__(self) -> None:
        Config.load_config()
        self.rules_path = Path('analyser/rules_specifications')

    def execute_all(self, filter=None) -> None:
        """
            Execute each QA rules.

            If a filter is given as parameter, the rules inside this
            filter wont be executed.
        """
        for rule_file in self.rules_path.glob('*.yaml'):
            if not filter or rule_file.stem not in filter:
                self.execute_one(rule_file.stem)

    def execute_one(self, name: str) -> None:
        """
            Execute one QA rule based on its YAML file name.
        """
        timer = Timer().start_timer()
        loaded_yaml: Dict = load_yaml_rule(name)
        PipelineAssembler(loaded_yaml, name).assemble().process_and_next()
        LOG.info('<%s> The whole rule executed in %s mins %s secs', name, *timer.get_elapsed())
