from __future__ import annotations
from analyser.core.dynamic_value import resolve_all
from typing import Dict
from analyser.core import Pipe
from geojson import Feature

class GeoJSONFeatureConverter(Pipe):
    """
        Handle the conversion of generic data class
        to geojson features.
    """
    def on_created(self) -> None:
        self.properties_pattern: Dict = self.extract_data('properties', default={})
        self.current_id = -1

    def process(self, elements: Dict) -> Feature:
        """
            Convert a query result to a geojson feature.
        """
        properties = dict()
        self.current_id += 1
        if self.properties_pattern:
            for prop in self.properties_pattern:
                #Resolve dynamic values
                resolved_value = resolve_all(prop, elements)
                for k, v in resolved_value.items():
                    properties[k] = v
        returned_geom = elements.pop('geometry_holder').to_geojson_feature(self.current_id, properties)
        return returned_geom