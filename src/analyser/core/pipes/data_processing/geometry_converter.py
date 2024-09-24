from __future__ import annotations
import importlib
from typing import Dict
from analyser.core import Pipe

class GeometryConverter(Pipe):
    """
        Pipe used to convert data to a Geometry class.
    """
    def on_created(self) -> None:
        self.geometry_type = self.extract_data('geometry_type', required=True)

    def process(self, data: Dict) -> Dict:
        """
            Converts the given Well-Known Text representation of a
            geometry into a Geometry class based on the geometry_type.
        """
        #If one data doesn't contain a geometry_holder it should be ignored.
        if (data['geometry_holder'] is None):
            return None
        module = importlib.import_module('analyser.core.model')
        dclass = getattr(module, self.geometry_type)
        convert = getattr(dclass, 'create_from_WKT_string')
        data['geometry_holder'] = convert(data['geometry_holder'])
        return data