from __future__ import annotations
from geojson.feature import Feature, FeatureCollection
from geojson import dumps
from analyser.logger.logger import LOG
from analyser.logger.timer import Timer
from analyser.core.model import Paths
from analyser.core import Pipe
from pathlib import Path
from typing import List
import typing
import subprocess

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

    def process(self, features: List[Feature]) -> Paths:
        """
            Converts a GeoJSON file to Vector tiles by
            calling tippecanoe from the command line.
        """
        feature_collection = FeatureCollection(features)
        output_dir = Path(self.base_folder_path / Path(self.folder_name))
        output_dir.mkdir(parents=True, exist_ok=True)
        timer = Timer().start_timer()

        try:
            result = subprocess.run(
                ['tippecanoe', f'--output-to-directory={output_dir}', 
                '--force',
                '--no-tile-compression',
                '-zg',
                '-K 60',
                '-r1',
                '--drop-densest-as-needed'],
                check=True,
                input=dumps(feature_collection).encode(),
                stdout=subprocess.PIPE
            )
            LOG.info(result)
        except subprocess.TimeoutExpired as e:
            LOG.fatal(e)
        except subprocess.CalledProcessError as e:
            LOG.fatal(e)

        LOG.info('Vector tile conversion executed in %s mins %s secs', *timer.get_elapsed())
        web_path = FULL_PATH_PREFIX + '/' + self.folder_name + '/{z}/{x}/{y}.pbf'
        return Paths(web_path, str(output_dir.resolve()))
    
    @staticmethod
    def create_from_node_data(data: dict, exec_context: ExecutionContext) -> VectorTileConverter:
        """
            Assembles the pipe with the given node data.
        """
        return VectorTileConverter(data['folder_name'], exec_context)