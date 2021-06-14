from pathlib import Path
from geojson import Feature
from geojson import FeatureCollection, dump
from geojson.geometry import Geometry

FULL_PATH_PREFIX = 'https://QA-data/geojson'

class GeoJSONFormatter():
    """
        Handles the creation of the GeoJSON file.
    """
    def __init__(self) -> None:
        self.features = []
        self.base_folder_path = Path('/srv/nominatim/data-files/geojson')
        self.sub_folder = ''

    def add_feature(self, geometry: Geometry) -> None:
        """
            Create a feature and add it to the global list.
        """
        self.features.append(Feature(geometry=geometry, id=len(self.features)))

    def process(self, filename: str) -> Path:
        """
            Create the FeatureCollection and dump it to
            a new GeoJSON file.
        """
        feature_collection = FeatureCollection(self.features)

        folder_path = Path(self.base_folder_path / Path(self.sub_folder)).resolve()
        folder_path.mkdir(parents=True, exist_ok=True)
        full_path = folder_path / Path(filename + '.json')

        with open(full_path, 'w') as file:
            dump(feature_collection, file)

        return Path(FULL_PATH_PREFIX / Path(self.sub_folder) / Path(filename + '.json'))
