from abc import abstractmethod
from dataclasses import dataclass
from geojson.feature import Feature
from .element import Element

@dataclass
class Geometry(Element):
    @abstractmethod
    def to_geojson_feature(self, id: int, properties: dict = {}) -> Feature:
        return