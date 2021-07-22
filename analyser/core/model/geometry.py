from __future__ import annotations
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from geojson.feature import Feature

@dataclass
class Geometry(metaclass=ABCMeta):
    @abstractmethod
    def to_geojson_feature(self, id: int, properties: dict = {}) -> Feature:
        return

    @staticmethod
    @abstractmethod
    def create_from_WKT_string(geom: str) -> Geometry:
        """
            Parse a WKT geometry to instantiate a new
            Geometry class.
        """
        return