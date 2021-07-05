from __future__ import annotations
from analyser.core.exceptions.yaml_syntax_exception import YAMLSyntaxException
from analyser.core.model.additionnal_data import AdditionalData
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
    def __init__(self, exec_context: ExecutionContext, properties_pattern: dict = None) -> None:
        super().__init__(exec_context)
        self.properties_pattern = properties_pattern

    def convert_to_geojson_feature(self, elements: dict, id: int) -> Feature:
        """
            Convert a query result to a geojson feature.
        """
        properties = dict()
        #If a custom propertie with the '$' syntax is used
        #find the corresponding name into the data record.
        if self.properties_pattern:
            for k, v in self.properties_pattern.items():
                if v[0] == '$':
                    name = v[1:]
                    if not name in elements:
                        raise YAMLSyntaxException(f'The {name} value doesn\'t exist.')
                    properties[k] = elements[name]
                else:
                    properties[k] = v
        return elements.pop(0).to_geojson_feature(id, properties)

    def process(self, all_elements: List[dict]) -> List[Feature]:
        """
            Convert multiple elements
            to a list of features.
        """
        features = list()
        for i, elements in enumerate(all_elements):
            features.append(self.convert_to_geojson_feature(elements, i))
        return features
    
    @staticmethod
    def create_from_node_data(data: dict, exec_context: ExecutionContext) -> GeoJSONFeatureConverter:
        """
            Assembles the pipe with the given node data.
        """
        properties = data['properties'] if 'properties' in data else None
        return GeoJSONFeatureConverter(exec_context, properties)