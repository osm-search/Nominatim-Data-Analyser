"""
    Module containing all pipes of the analyser.
"""

from .filling_pipe import FillingPipe as FillingPipe

from .output_formatters.geojson_formatter import GeoJSONFormatter as GeoJSONFormatter
from .output_formatters.geojson_feature_converter import GeoJSONFeatureConverter as GeoJSONFeatureConverter
from .output_formatters.vector_tile_formatter import VectorTileFormatter as VectorTileFormatter
from .output_formatters.osmoscope_layer_formatter import OsmoscopeLayerFormatter as OsmoscopeLayerFormatter
from .output_formatters.clusters_vt_formatter import ClustersVtFormatter as ClustersVtFormatter

from .data_fetching.sql_processor import SQLProcessor as SQLProcessor

from .rules_specific_pipes.addr_house_number_no_digit.digits_filter import AddrHouseNumberNoDigitFilter as AddrHouseNumberNoDigitFilter
from .rules_specific_pipes.duplicate_label_role.custom_feature_converter import DuplicateLabelRoleCustomFeatureConverter as DuplicateLabelRoleCustomFeatureConverter
from .rules_specific_pipes.place_nodes_close.custom_feature_converter import PlaceNodesCloseCustomFeatureConverter as PlaceNodesCloseCustomFeatureConverter
from .rules_specific_pipes.same_wikidata.custom_feature_converter import SameWikiDataFeatureConverter as SameWikiDataFeatureConverter

from .data_processing.loop_data_processor import LoopDataProcessor as LoopDataProcessor
from .data_processing.geometry_converter import GeometryConverter as GeometryConverter
