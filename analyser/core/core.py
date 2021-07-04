from analyser.logger.logger import LOG
from analyser.logger.timer import Timer
import os
from pathlib import Path
from analyser.core.assembler import RuleAssembler

class Core():
    """
        Core of the analyser used to execute rules.
    """
    def execute_all(self) -> None:
        """
            Execute each QA rules.
        """
        rules_path = Path('analyser/rules_specifications').resolve()
        for rule in os.listdir(str(rules_path)):
            file_without_ext = os.path.splitext(rule)[0]
            self.execute_one(file_without_ext)

    def execute_one(self, name: str) -> None:
        """
            Execute one QA rule based on its YAML file name.
        """
        timer = Timer().start_timer()
        RuleAssembler(name).assemble().process_and_next()
        LOG.info('Rule %s executed in %s mins %s secs', name, *timer.get_elapsed())