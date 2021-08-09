from __future__ import annotations
from geojson.feature import Feature, FeatureCollection
from geojson import dumps
from analyser.logger.timer import Timer
from analyser.config import Config
from analyser.core import Pipe
from pathlib import Path
from typing import List
import subprocess
import logging

class VectorTileFormatter(Pipe):
    """
        Handles the creation of the GeoJSON file.
    """
    def on_created(self) -> None:
        self.base_folder_path = Path(f'{Config.values["RulesFolderPath"]}/{self.exec_context.rule_name}/vector-tiles')

    def process(self, features: List[Feature]) -> str:
        """
            Converts a GeoJSON file to Vector tiles by
            calling tippecanoe from the command line.
        """
        feature_collection = FeatureCollection(features)
        self.base_folder_path.mkdir(parents=True, exist_ok=True)
        timer = Timer().start_timer()

        self.call_tippecanoe(self.base_folder_path, feature_collection)

        elapsed_mins, elapsed_secs = timer.get_elapsed()
        self.log(f'Vector tile conversion executed in {elapsed_mins} mins {elapsed_secs} secs')

        web_path = f'{Config.values["WebPrefixPath"]}/{self.exec_context.rule_name}/vector-tiles/' + '{z}/{x}/{y}.pbf'
        return web_path
    
    def call_tippecanoe(self, output_dir: Path, feature_collection: FeatureCollection) -> None:
        """
            Calls Tippecanoe through a subprocess and send the feature collection as a stream
            in the stdin of the subprocess.
        """
        try:
            result = subprocess.run(
                ['tippecanoe', f'--output-to-directory={output_dir}', 
                '--force',
                '--no-tile-compression',
                '-r1',
                '-K 20',
                '-B10'],
                check=True,
                input=dumps(feature_collection).encode(),
                stdout=subprocess.PIPE
            )
            self.log(result)
        except subprocess.TimeoutExpired as e:
            self.log(logging.FATAL, e)
        except subprocess.CalledProcessError as e:
            self.log(logging.FATAL, e)