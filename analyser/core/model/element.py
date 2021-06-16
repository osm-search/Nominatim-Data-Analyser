from abc import abstractmethod
from dataclasses import dataclass

from geojson.feature import Feature

@dataclass
class Element:
    properties: dict()

    @abstractmethod
    def to_geojson_feature(self, id: int) -> Feature:
        pass