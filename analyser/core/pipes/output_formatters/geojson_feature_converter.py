from __future__ import annotations
from typing import Dict
from analyser.core.yaml_logic.complex_value_parser import parse_complex_value
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
        #If a custom propertie with the '$' syntax is used
        #find the corresponding name into the data record.
        if self.properties_pattern:
            for item in self.properties_pattern.items():
                parsed_value = parse_complex_value(item, elements)
                #A dictionnary is returned if there was a /?nwr?/ condition
                #else the tuple is returned.
                if isinstance(parsed_value, dict):
                    for k, v in parsed_value.items():
                        properties[k] = v
                else:
                    properties[parsed_value[0]] = parsed_value[1]
        returned_geom = elements.pop('geometry_holder').to_geojson_feature(self.current_id, properties)
        return returned_geom