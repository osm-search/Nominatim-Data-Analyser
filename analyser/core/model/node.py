from __future__ import annotations
from geojson.feature import Feature
from geojson.geometry import Point
from analyser.core.model import Element
from dataclasses import dataclass
import re

@dataclass
class Node(Element):
    coordinates: list()

    def to_geojson_feature(self, id: int) -> Feature:
        """
            Return this Node as a geojson feature.
        """
        point = Point(coordinates=self.coordinates)
        feature = Feature(geometry=point, properties=self.properties, id=id)
        return feature

    @staticmethod
    def create_from_string(geom: str) -> Node:
        """
            Parse a WKT geometry to instantiate a new
            Node class.
        """
        pattern = "POINT\((.*) (.*)\)"
        results = re.match(pattern, geom)
        coordinates = [float(results[1]), float(results[2])]
        return Node({}, coordinates)