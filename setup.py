from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension

ext_modules = [
    Pybind11Extension(
        "nominatim_data_analyser.clustering_vt",
        ["clustering-vt/clustering-vt.cpp"],
        include_dirs=[
            "contrib/geojson/0.4.3/include",
            "contrib/protozero/1.7.0/include",
            "contrib/geometry/1.0.0/include",
            "contrib/vtzero/1.1.0/include",
            "contrib/kdbush/0.1.3/include",
            "contrib/supercluster/0.3.2/include",
            "contrib/variant/1.2.0/include",
            "contrib/rapidjson/1.1.0/include",
        ],
        cxx_std=17
    ),
]

setup(ext_modules=ext_modules)
