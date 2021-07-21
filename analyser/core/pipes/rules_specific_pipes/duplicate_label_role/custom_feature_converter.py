from analyser.core.pipe import Pipe
from geojson.feature import Feature
from typing import List

class DuplicateLabelRoleCustomFeatureConverter(Pipe):
    def process(self, data: List[dict]) -> List[Feature]:
        """
            Creates Geojson features for each result from the SQLProcessor.

            Extract members with role=label from the list of members
            returned by the table planet_osm_rels to display them in
            the properties of the Node.

            The members array has the following syntax:
            ['w8125151','outer','w249285853','inner'.......]
            It works by pair where the first item ('w8125151' for example)
            contains the object type (n, w, r) and its osm_id, then 
            the second item is the role ('outer' for example).
        """
        features: List[Feature] = list()
        current_feature_id = 0
        for record in data:
            properties = {
                'relation_id': record['osm_id']
            }
            members = record['members']
            label_members_count = 0
            for i in range(len(members) - 1):
                role = members[i+1]
                if role == 'label':
                    label_members_count += 1
                    #Get the n/w/r type
                    type = members[i][0]
                    properties[f'{type}/@idLabel {label_members_count}'] = members[i][1:]
        
            features.append(record.pop(0).to_geojson_feature(current_feature_id, properties))
            current_feature_id += 1
        return features