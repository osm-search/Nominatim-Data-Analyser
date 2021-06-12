from abc import ABC, abstractmethod
from analyser.logic.formatters import GeoJSONFormatter
from analyser.logic.formatters import LayerFormatter

class BaseRule():
    """
        Base class for a QA rule.
    """
    def __init__(self) -> None:
        super().__init__()
        self.layer_formatter = self.construct_layer_formatter()
        self.geojson_formatter = GeoJSONFormatter()

    @abstractmethod
    def execute(self) -> bool:
        """
            Execute this QA rule.
        """
        pass

    @abstractmethod
    def construct_layer_formatter(self) -> LayerFormatter:
        """
            Construct the layer formatter object with
            the right layer informations.
        """
        pass
