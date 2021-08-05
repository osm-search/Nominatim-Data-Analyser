from analyser.core.model.paths import Paths
from analyser.config import Config
from analyser.core.pipes import OsmoscopeLayerFormatter
import json

def test_add_layer_to_global_layers_file_doesnt_exist(osmoscope_layer_formatter: OsmoscopeLayerFormatter,
                                                      config: Config,
                                                      tmp_path) -> None:
    """
        Test the add_layer_to_global_layers_file() method with a layers.json which doesnt exist yet.
        It should be created and the layer added to it.
    """
    config.values['RulesFolderPath'] = tmp_path / 'test_folder'
    osmoscope_layer_formatter.add_layer_to_global_layers_file('test/test_layer_path.json')
    with open(tmp_path / 'test_folder/layers.json', 'r') as file:
        data = json.load(file)
    assert data['layers'] == ['test/test_layer_path.json']

def test_add_layer_to_global_layers_file_exist(osmoscope_layer_formatter: OsmoscopeLayerFormatter,
                                               config: Config,
                                               tmp_path) -> None:
    """
        Test the add_layer_to_global_layers_file() method with a layers.json already exist.
        The new layer should be added to the file.
    """
    config.values['RulesFolderPath'] = tmp_path
    #Create an initial layers.json with one layer inside.
    data = {
        'name': 'Nominatim suspects',
        'layers': ['layer_already_in']
    }
    full_path = tmp_path / 'layers.json'
    full_path.touch(exist_ok=True)
    with open(full_path, 'w') as json_file:
        json.dump(data, json_file)

    osmoscope_layer_formatter.add_layer_to_global_layers_file('test/test_layer_path.json')

    with open(full_path, 'r') as file:
        data = json.load(file)
    assert data['layers'] == ['layer_already_in', 'test/test_layer_path.json']

def test_process_osmoscope_layer_formatter(osmoscope_layer_formatter: OsmoscopeLayerFormatter,
                                           tmp_path) -> None:
    """
        Test the process() method.
        The layer file should be created with the right data inside.
    """
    osmoscope_layer_formatter.base_folder_path = tmp_path / 'test_folder'
    osmoscope_layer_formatter.data = dict()
    osmoscope_layer_formatter.data['id'] = 'test_id'
    osmoscope_layer_formatter.file_name = 'test_file'
    osmoscope_layer_formatter.data_format_url = 'vector_tile_url'
    paths = Paths('web_path', 'local_path')
    osmoscope_layer_formatter.process(paths)

    with open(tmp_path / 'test_folder/test_file.json', 'r') as file:
        data = json.load(file)
    assert data == {
        'id': 'test_id',
        'vector_tile_url': paths.web_path
    }
