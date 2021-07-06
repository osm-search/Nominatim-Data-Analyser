from __future__ import annotations
from analyser.logger.logger import LOG
from analyser.logger.timer import Timer
from analyser.core.model import Paths
from analyser.core import Pipe
from pathlib import Path
import os
import typing

if typing.TYPE_CHECKING:
    from analyser.core.qa_rule import ExecutionContext

FULL_PATH_PREFIX = 'https://gsoc2021-qa.nominatim.org/QA-data/vector-tiles'

class VectorTileConverter(Pipe):
    """
        Handles the creation of the GeoJSON file.
    """
    def __init__(self, folder_name: str, exec_context: ExecutionContext) -> None:
        super().__init__(exec_context)
        self.base_folder_path = Path('/srv/nominatim/data-files/vector-tiles')
        self.folder_name = folder_name

    def process(self, geojson_paths: Paths) -> Paths:
        """
            Converts a GeoJSON file to Vector tiles by
            calling tippecanoe from the command line.
        """
        output_dir = Path(self.base_folder_path / Path(self.folder_name))
        output_dir.mkdir(parents=True, exist_ok=True)
        timer = Timer().start_timer()

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
        
        LOG.info('Vector tile conversion executed in %s mins %s secs', *timer.get_elapsed())
        web_path = FULL_PATH_PREFIX + '/' + self.folder_name + '/{z}/{x}/{y}.pbf'
        return Paths(web_path, str(output_dir.resolve()))
    
    @staticmethod
    def create_from_node_data(data: dict, exec_context: ExecutionContext) -> VectorTileConverter:
        """
            Assembles the pipe with the given node data.
        """
        return VectorTileConverter(data['folder_name'], exec_context)