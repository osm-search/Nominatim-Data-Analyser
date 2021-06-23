from __future__ import annotations
from geojson.feature import Feature
from geojson.geometry import Point
from .element import Element
from .geometry import Geometry
from dataclasses import dataclass
import re

@dataclass
class Node(Geometry):
    coordinates: list()

    def to_geojson_feature(self, id: int, properties: dict = {}) -> Feature:
        """
            Return this Node as a geojson feature.
        """
        point = Point(coordinates=self.coordinates)
        feature = Feature(geometry=point, properties=properties, id=id)
        return feature

    @staticmethod
    def create_from_WKT_string(geom: str) -> Node:
        """
            Parse a WKT geometry to instantiate a new
            Node class.
        """
        pattern = "POINT\((.*) (.*)\)"
        results = re.match(pattern, geom)
        coordinates = [float(results[1]), float(results[2])]
        return Node(coordinates)

    @staticmethod
    def create_from_sql_result(result: any, *args) -> Element:
        """
            Return a Node based on an SQL result.
        """
        return Node.create_from_WKT_string(result)
