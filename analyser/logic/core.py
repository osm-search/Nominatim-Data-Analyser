
from analyser.logic.rules import AdminBoundNoAdminLevel
from analyser.logic import BaseRule
from typing import Set

class Core():
    """
        Core of the analyser. 
        Register and execute QAUnits.
    """
    def __init__(self) -> None:
        self.rules: Set[BaseRule] = set()
        self.register_qa_unit(AdminBoundNoAdminLevel())

    def register_qa_unit(self, qa_unit: BaseRule) -> None:
        """
            Add one QA Unit to the list of those
            to be executed.
        """
        self.rules.add(qa_unit)

    def execute_all(self) -> None:
        """
            Execute each QAUnit.
        """
        for unit in self.rules:
            unit.execute()