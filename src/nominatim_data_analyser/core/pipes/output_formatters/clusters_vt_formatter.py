from __future__ import annotations
from geojson.feature import Feature, FeatureCollection
from geojson import dumps
from ....logger.timer import Timer
from ....config import Config
from ... import Pipe
from ....clustering_vt import cluster
from pathlib import Path
from typing import List
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
        result = cluster(str(output_dir), self.radius, (dumps(feat) for feat in feature_collection['features']))
        if result != 0:
            raise RuntimeError("Clustering failed.")
