from geojson.geometry import Point
from analyser.logic.formatters import LayerFormatter
from analyser.logic.base_rule import BaseRule
from analyser.database import connect
from analyser.logic import BaseRule
from geojson import Polygon
import json

class AdminBoundNoAdminLevel(BaseRule):
    """
        Implements the rule:

        "Relations with boundary=administrative without admin_level"
    """
    def __init__(self) -> None:
        super().__init__()

    def execute(self) -> bool:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT ST_AsGeoJSON(geometry) FROM placex WHERE osm_type='R' AND class='boundary'
                    AND type='administrative' AND admin_level >= 15 LIMIT 5;
                """)
                for geom in cur:
                    loaded = json.loads(geom[0])
                    self.geojson_formatter.add_feature(Polygon(coordinates=loaded['coordinates']))
                
                #Tests purpose only
                self.geojson_formatter.add_feature(Point((-122.789597, 49.195354)))

        geojson_path = self.geojson_formatter.process('AdminBoundNoAL')
        self.layer_formatter.set_geojson_url(str(geojson_path))
        self.layer_formatter.process()
        return True

    def construct_layer_formatter(self) -> LayerFormatter:
        return LayerFormatter(
            'AdminBoundNoAdminLevel',
            'Every evening'
        ).add_doc(
            'description', 'Every relation with boundary=administrative'\
            'should have a correct admin_level value set.'
        ).add_doc(
            'how_to_fix', 'An admin_level value should be set to the relation.'
        )
