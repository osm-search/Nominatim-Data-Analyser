from ....pipe import Pipe
from typing import List
from ....model.node import Node
from geojson import Feature

class SameWikiDataFeatureConverter(Pipe):
    def process(self, data: List[dict]) -> List[Feature]:
        """
            Creates Geojson features for each nodes.
            each result from the SQLProcessor contains
            multiple nodes.

            data is a list of list of format:
            [wikidata, List[ids], List[centroids]]
        """
        features: List[Feature] = list()
        current_feature_id = 0
        for record in data:
            for i, centroid in enumerate(record['centroids']):
                #If one centroid is None the data should be ignored.
                if (centroid is None):
                    continue
                node = Node.create_from_WKT_string(centroid)
                nodes_in_common = list()
                #Fetch concerning node id and id of each other nodes with the
                #same wikidata
                for j, id in enumerate(record['ids']):
                    if j == i:
                        node_id = id
                    else:
                        nodes_in_common.append(id)
                properties = {
                    'node_id': node_id,
                    'wikidata in common': record['wikidata']
                }
                for i, id in enumerate(nodes_in_common):
                    properties['n/@idNode in common ' + str(i + 1)] = id
                features.append(node.to_geojson_feature(current_feature_id, properties))
                current_feature_id += 1
        return features

