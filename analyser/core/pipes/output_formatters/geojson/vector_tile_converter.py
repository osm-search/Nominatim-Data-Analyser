from __future__ import annotations
from analyser.core.model import Paths
from analyser.core import Pipe
from pathlib import Path
from geojson import FeatureCollection, dumps
from geojson2vt.geojson2vt import geojson2vt
import os
import typing

if typing.TYPE_CHECKING:
    from analyser.core.qa_rule import ExecutionContext

FULL_PATH_PREFIX = 'https://QA-data/vector-tiles'

class VectorTileConverter(Pipe):
    """
        Handles the creation of the GeoJSON file.
    """
    def __init__(self, filename: str, exec_context: ExecutionContext) -> None:
        super().__init__(exec_context)
        self.base_folder_path = Path('/srv/nominatim/data-files/vector-tiles')
        self.sub_folder = ''
        self.file_name = filename

    def process(self, geojson_paths: Paths) -> str:
        """
            Convert a GeoJSON file to Vector tiles by
            calling tippecanoe from the command line.
        """
        output_dir = Path(self.base_folder_path / Path('layer'))
        os.system(f"""
            tippecanoe --output-to-directory {output_dir} \
            --no-tile-compression \
            --generate-ids \
            --layer=layer \
            --name="New Layer" \
            --description="Description of new layer" \
            --attribution='Copyright OpenStreetMap contributors' \
            --base-zoom=6 \
            --maximum-tile-bytes=50000 \
            --drop-densest-as-needed \
            --quiet \
            --force \
            {geojson_paths.local_path}
        """)

        return Paths(str(Path(FULL_PATH_PREFIX / Path('layer/{z}/{x}/{y}.pbf'))))
    
    @staticmethod
    def create_from_node_data(data: dict, exec_context: ExecutionContext) -> VectorTileConverter:
        """
            Assembles the pipe with the given node data.
        """
        return VectorTileConverter(data['file_name'], exec_context)