from analyser.core.pipe import Pipe
from geojson.feature import Feature
from typing import List

class PlaceNodesCloseCustomFeatureConverter(Pipe):
    def process(self, data: List[dict]) -> List[Feature]:
        """
            Creates Geojson features for each result from the SQLProcessor.
        """
        features: List[Feature] = list()
        current_feature_id = 0
        for record in data:
            properties = {
                'node_id': record['osm_id']
            }
            common_ids = record['common_ids']
            for i in range(len(common_ids)):
                properties[f'n/@idClose node {i+1}'] = common_ids[i]
        
            features.append(record.pop(0).to_geojson_feature(current_feature_id, properties))
            current_feature_id += 1
        return features