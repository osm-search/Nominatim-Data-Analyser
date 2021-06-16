from typing import List
from analyser.core.pipe import Pipe
from analyser.core.model import Element
from geojson import Feature

class GeoJSONFeatureConverter(Pipe):
    """
        Handle the conversion of generic data class
        to geojson features.
    """
    def __init__(self) -> None:
        super().__init__()

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
            features.append(self.convert_to_geojson_feature(element, i))
        return features