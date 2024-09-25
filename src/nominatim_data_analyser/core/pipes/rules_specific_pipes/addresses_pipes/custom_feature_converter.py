from ....pipe import Pipe
from geojson.feature import Feature
from typing import Dict

class AddressesCustomFeatureConverter(Pipe):
    def on_created(self) -> None:
        self.current_feature_id = -1

    # def process(self, elements: Dict) -> Feature:
    #     """
    #         Creates Geojson features for the given result of the SQLProcessor.

    #         Extract each values of the address and set it as a property.
    #     """
    #     types_mapping = {
    #         'N': 'node_id',
    #         'W': 'way_id',
    #         'R': 'relation_id'
    #     }
    #     self.current_feature_id += 1
    #     properties = {
    #         types_mapping[elements['osm_type']]: elements['osm_id']
    #     }
    #     address = elements['address']
    #     for a in address:
    #         print(a)
    
    #     return elements.pop('geometry_holder').to_geojson_feature(self.current_feature_id, properties)
