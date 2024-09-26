from typing import Any
from .....core.pipe import Pipe
from geojson.feature import Feature

class PlaceNodesCloseCustomFeatureConverter(Pipe):
    def on_created(self) -> None:
        self.current_feature_id = -1

    def process(self, elements: dict[str, Any]) -> Feature:
        """
            Creates a Geojson feature for the given elements dictionnary.
            Adds a specific property for each id in the 'common_ids' field.
        """
        self.current_feature_id += 1

        properties = {
            'node_id': elements['osm_id']
        }
        common_ids = elements['common_ids']
        for i in range(len(common_ids)):
            properties[f'n/@idClose node {i+1}'] = common_ids[i]

        return elements.pop('geometry_holder').to_geojson_feature(self.current_feature_id, properties)
