from analyser.core.pipe import Pipe
from geojson.feature import Feature
from typing import Dict

class PlaceNodesCloseCustomFeatureConverter(Pipe):
    def on_created(self) -> None:
        self.current_feature_id = -1

    def process(self, elements: Dict) -> Feature:
        """
            Creates Geojson features for the given result from the SQLProcessor.
        """
        self.current_feature_id += 1

        properties = {
            'node_id': elements['osm_id']
        }
        common_ids = elements['common_ids']
        for i in range(len(common_ids)):
            properties[f'n/@idClose node {i+1}'] = common_ids[i]

        return elements.pop('geometry_holder').to_geojson_feature(self.current_feature_id, properties)