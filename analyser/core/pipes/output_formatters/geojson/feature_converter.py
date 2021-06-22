from __future__ import annotations
from typing import List
from analyser.core import Pipe
from analyser.core.model import Element
from geojson import Feature
import typing

if typing.TYPE_CHECKING:
    from analyser.core.qa_rule import ExecutionContext

class GeoJSONFeatureConverter(Pipe):
    """
        Handle the conversion of generic data class
        to geojson features.
    """
    def convert_to_geojson_feature(self, element: Element, id: int) -> Feature:
        """
            Convert a generic data class to a
            geojson feature.
        """
        return element.to_geojson_feature(id)

    def process(self, elements: List[Element]) -> List[Feature]:
        """
            Convert multiple elements 
            to a list of features.
        """
        features = list()
        for i, element in enumerate(elements):
            features.append(self.convert_to_geojson_feature(element[0], i))
        return features
    
    @staticmethod
    def create_from_node_data(data: dict, exec_context: ExecutionContext) -> GeoJSONFeatureConverter:
        """
            Assembles the pipe with the given node data.
        """
        return GeoJSONFeatureConverter(exec_context)