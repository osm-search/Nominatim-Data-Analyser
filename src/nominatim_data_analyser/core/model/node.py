from geojson.feature import Feature
from geojson.geometry import Point
from .geometry import Geometry
from dataclasses import dataclass
import re

@dataclass
class Node(Geometry):
    coordinates: list[float]

    def to_geojson_feature(self, id: int, properties: dict[str, str]) -> Feature:
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
        if results is None:
            raise RuntimeError("Not a valid WKT.")
        coordinates = [float(results[1]), float(results[2])]
        return Node(coordinates)
