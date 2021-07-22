from analyser.core.yaml_logic.yaml_loader import load_yaml_rule
from analyser.core.assembler.pipeline_assembler import PipelineAssembler
from analyser.config.config import Config
from analyser.logger.logger import LOG
from analyser.logger.timer import Timer
from pathlib import Path
from typing import Dict
import os

class Core():
    """
        Core of the analyser used to execute rules.
    """
    def __init__(self) -> None:
        Config.load_config()

    def execute_all(self, filter=None) -> None:
        """
            Execute each QA rules.

            If a filter is given as parameter, the rules inside this
            filter wont be executed.
        """
        rules_path = Path('analyser/rules_specifications').resolve()
        for rule in os.listdir(str(rules_path)):
            file_without_ext = os.path.splitext(rule)[0]
            if not filter or file_without_ext not in filter:
                self.execute_one(file_without_ext)

    def execute_one(self, name: str) -> None:
        """
            Execute one QA rule based on its YAML file name.
        """
        timer = Timer().start_timer()
        loaded_yaml: Dict = load_yaml_rule(name)
        PipelineAssembler(loaded_yaml, name).assemble().process_and_next()
        LOG.info('Rule <%s> : The whole rule executed in %s mins %s secs', name, *timer.get_elapsed())