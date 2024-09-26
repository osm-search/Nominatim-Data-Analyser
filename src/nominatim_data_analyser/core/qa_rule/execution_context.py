class ExecutionContext():
    """
        Execution context of a QA Rule pipeline
        which contains data and objects.

        It is stored in each pipe of the QA Rule pipeline.
    """
    def __init__(self) -> None:
        self.rule_name = ''
