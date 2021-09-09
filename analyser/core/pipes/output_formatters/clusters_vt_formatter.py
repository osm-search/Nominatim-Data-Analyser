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

class ClustersVtFormatter(Pipe):
    """
        Handles the creation of the clusters and vector tiles.
    """
    def on_created(self) -> None:
        self.base_folder_path = Path(f'{Config.values["RulesFolderPath"]}/{self.exec_context.rule_name}/vector-tiles')
        self.radius: int = self.extract_data('radius', default=60)

    def process(self, features: List[Feature]) -> str:
        """
            Converts a list of GeoJSON features to clusters vector tiles by
            calling clustering-vt from the command line.

            The outputfolder is initially deleted if it exists.
        """
        feature_collection = FeatureCollection(features)
        timer = Timer().start_timer()

        self.call_clustering_vt(self.base_folder_path, feature_collection)

        elapsed_mins, elapsed_secs = timer.get_elapsed()
        self.log(f'Clustering and vector tiles creation executed in {elapsed_mins} mins {elapsed_secs} secs')

        web_path = f'{Config.values["WebPrefixPath"]}/{self.exec_context.rule_name}/vector-tiles/' + '{z}/{x}/{y}.pbf'
        return web_path
    
    def call_clustering_vt(self, output_dir: Path, feature_collection: FeatureCollection) -> None:
        """
            Calls clustering-vt through a subprocess and send the feature collection as a stream
            in the stdin of the subprocess.
        """
        try:
            result = subprocess.run(
                [f'{Path(__file__).parent.resolve()}/../../../../clustering-vt/build/clustering-vt', output_dir, str(self.radius)],
                check=True,
                input=dumps(feature_collection, sort_keys=True).encode(),
                capture_output=True
            )
            self.log(result)
        except subprocess.TimeoutExpired as e:
            self.log(e, logging.FATAL)
        except subprocess.CalledProcessError as e:
            self.log(e, logging.FATAL)