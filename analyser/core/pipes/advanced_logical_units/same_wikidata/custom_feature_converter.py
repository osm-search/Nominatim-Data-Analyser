from typing import List
from analyser.core.model.node import Node
from analyser.core.pipes.advanced_logical_units import AdvancedLogicalUnit
from geojson.geometry import Point
from geojson import Feature

class SameWikiDataFeatureConverter(AdvancedLogicalUnit):
    def process(self, data: any = None) -> any:
        """
            Creates Geojson features for each nodes.
            each result from the SQLProcessor contains
            multiple nodes.

            data is a list of list of format:
            [wikidata, List[ids], List[centroids]]
        """
        features: List[Feature] = list()
        current_feature_id = 0
        for additional_data in data:
            for i, centroid in enumerate(additional_data[2].data):
                node = Node.create_from_WKT_string(centroid)
                nodes_in_common = list()
                #Fetch concerning node id and id of each other nodes with the
                #same wikidata
                for j, id in enumerate(additional_data[1].data):
                    if j == i:
                        node_id = id
                    else:
                        nodes_in_common.append(id)
                properties = {
                    'node_id': node_id,
                    'wikidata in common': additional_data[0].data
                }
                for i, id in enumerate(nodes_in_common):
                    properties['Node in common ' + str(i)] = id
                features.append(node.to_geojson_feature(current_feature_id, properties))
                current_feature_id += 1
        return features

