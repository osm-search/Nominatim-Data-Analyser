# The Pipe base class

## Overview

The `Pipe` base class is inherited from all other pipes. It contains the main logic needed to construct a custom `pipe`.
This class can be found in `analyser/core/pipe.py`.

It contains a set of `pipes` which are plugged to it. Multiple `pipes` can be plugged to one `pipe`.

## Methods

### process

The process() method is the main method of the `Pipe` class. It is an abstract method which should be overriden in child `Pipe` classes and which defines the execution process of the `pipe`.
This method as the following definition in the `Pipe` class:

```python
@abstractmethod
def process(self, data: any = None) -> any:
    """
        Contains the execution logic of this pipe.
    """
    return
```

This is the main method of the `Pipe` class which takes data as parameters (often data sent from previous `pipes`), processes them and returns them (to often send them to next `pipes`).

### process_and_next

The `process_and_next` method runs the `process` method of the pipe and then executes all of the plugged `pipes` in order by sending them data returned by the `process` method.

### extract_data

The `extract_data` method is used to extract a value from the `data` dictionnary of the `pipe`. This `data` dictionnary is given as input when the `Pipe` class is instantiated. It contains all the data defined for this pipe in the [YAML Rule Specification](YAML-Rule-Specification.md).

If we have the following pipe specification in the YAML Rule Specification:

```yaml
GEOMETRY_CONVERTER:
    type: GeometryConverter
    geometry_type: Node
```

We can use this call to `extract_data`:

```python
self.geometry_type = self.extract_data('geometry_type', required=True)
```

This call will returns `"Node"`. Note the `required=True` which says that this field is required and if it can't be found by the `extract_data` method an `Exception` will be raised.

It is also possible to give a `default` argument. If the searched data is not found the `default` value will be returned.

### on_created

As all the `pipes` are automatically instantiated following a general schema, when creating a custom `pipe` the `on_created` method can be overriden to run some actions when the pipe is created. It is very convenient to call the `extract_data` method inside the `on_created` method:

```python
def on_created(self) -> None:
    self.geometry_type = self.extract_data('geometry_type', required=True)
```

### log

The `log` method is used to log messages by automatically adding a `prefix` with the `name` of the rule which is logging the message.

Example using the default logging level (INFO):

```python
self.log(f'Loop data processor executed in {elapsed_mins} mins {elapsed_secs} secs.')
```

Example using a specific logging level (FATAL):

```python
self.log(logging.FATAL, "Fatal log message.")
```

## Custom pipe example:

The `GeometryConverter` pipe is a good example on how to create a custom pipe:

```python
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
        module = importlib.import_module('analyser.core.model')
        dclass = getattr(module, self.geometry_type)
        convert = getattr(dclass, 'create_from_WKT_string')
        data['geometry_holder'] = convert(data['geometry_holder'])
        return data
```

The `on_created` method is overriden and used to set the `self.geometry_type` by calling the `extract_data` method. Then, the `process` method is doing all of the pipe's work.

# Main pipes

Here is a basic documentation for all the main pipes:

## SQLPProcessor

Executes an SQL query and returns the results as [RealDictCursor](https://www.psycopg.org/docs/extras.html#real-dictionary-cursor) objects.

**Class name (type)** -> `SQLProcessor`

**Mandatory fields**:

* `query` -> The SQL query to execute.

**Expected inputs** -> `None`

**Output** -> List of [RealDictCursor](https://www.psycopg.org/docs/extras.html#real-dictionary-cursor) objects.

## GeometryConverter

Converts the data contains in the `geometry_holder` of the input dictionnary to the geometry class of type `geometry_type`.

**Class name (type)** -> `GeometryConverter`

**Mandatory fields**:

* `geometry_type` -> The geometry type to use.

**Expected inputs** -> `Dictionnary` with one key equal to `geometry_holder` which should be a `string` of a [Well-known text representation of geometry](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry).

**Output** -> `Dictionnary` with the `geometry_holder` modified.

## LoopDataProcessor

Processes each `data` of the input list through a `sub pipeline` and returns the new list of `data`.

**Class name (type)** -> `LoopDataProcessor`

**Mandatory fields**:

* `sub_pipeline` -> A sub pipeline.

**Expected inputs** -> `List` of data of `any` type.

**Output** -> `List` of data of `any` type.

## GeoJSONFeatureConverter

Converts a dictionnary of data containing at least the `geometry_holder` field to a `GeoJSON Feature` from the [geojson python package](https://github.com/jazzband/geojson).

**Class name (type)** -> `GeoJSONFeatureConverter`

**Optional fields**:

* `properties` -> `Dictionnary` of properties to add to the generated `Feature`.

**Expected inputs** -> `Dictionnary` with one key equal to `geometry_holder` which contains a `Geometry` class (Often received from a previous `GeometryConverter` pipe).

**Output** -> [geojson python package](https://github.com/jazzband/geojson) object.

## GeoJSONFormatter

Generates a `GeoJSON file` from a list of [Feature](https://github.com/jazzband/geojson#feature).

**Class name (type)** -> `GeoJSONFormatter`

**Optional fields**:

* `file_name` -> The file name for the generated file.

**Expected inputs** -> `List` of [Feature](https://github.com/jazzband/geojson#feature).

**Output** -> (Subject to change).

## VectorTileFormatter

Generates a `Vector tile` folder with a hierarchy of vector tiles inside from a list of [Feature](https://github.com/jazzband/geojson#feature). This pipe makes a call to [Tippecanoe](https://github.com/mapbox/tippecanoe) to generate the vector tiles.

**Class name (type)** -> `VectorTileFormatter`

**Expected inputs** -> `List` of [Feature](https://github.com/jazzband/geojson#feature).

**Output** -> (Subject to change).

## OsmoscopeLayerFormatter

Generates a `Layer` file following the [Layer specification](https://github.com/osmoscope/osmoscope-ui/blob/master/doc/creating-layers.md#the-layer-file) of Osmoscope.

**Class name (type)** -> `OsmoscopeLayerFormatter`

**Optional fields**:

* `id` -> Id of the layer, should be only composed of [a-z0-9_] and it should be unique among all the rules. Default value if not provided is the name of the YAML file of this rule.
* `file_name` -> The file name for the generated file.
* `updates` -> When are the data updated.
* `doc` -> Dictionnary containing documentation of the layer:
    * `description` -> Description of the layer.
    * `why_problem` -> Why is there a problem with the data on this layer.
    * `how_to_fix` -> How to fix data on this layer.

**Mandatory fields**:

* `data_format_url` -> `geojson_url` or `vector_tile_url`.
* `name` -> The name of the rule.

**Expected inputs** -> (Subject to change).

**Output** -> `None`.