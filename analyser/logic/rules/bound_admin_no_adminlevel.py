from geojson.geometry import Polygon, Point
from analyser.logic.formatters import LayerFormatter
from analyser.logic.base_rule import BaseRule
from analyser.database import connect
from analyser.logic import BaseRule
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
                    SELECT ST_AsGeoJSON(ST_Centroid(geometry)) FROM placex WHERE osm_type='R' AND class='boundary'
                    AND type='administrative' AND admin_level >= 15;
                """)
                for geom in cur:
                    loaded = json.loads(geom[0])
                    self.geojson_formatter.add_feature(Point(coordinates=loaded['coordinates']))

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
