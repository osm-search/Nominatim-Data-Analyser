# YAML Rule Specification

A rule is defined inside a YAML Rule file. This file follows the YAML Rule Specification defined in this chapter.

# Introduction

The YAML Rule Specification follows a pipeline architecture (See [Architecture](Overview.md#architecture)). Hence, a specific format should be followed for the rule to work.

For example, here is the YAML Rule Specification for the rule `boundary=administrative without an admin_level value set`:

```yaml
---
- type: SQLProcessor
  query: >
    SELECT ST_AsText(centroid) AS geometry_holder, osm_id FROM placex WHERE osm_type='R' AND class='boundary'
    AND type='administrative' AND admin_level >= 15;

- type: LoopDataProcessor
  sub_pipeline: !sub-pipeline
    - type: GeometryConverter
      geometry_type: Node

    - type: GeoJSONFeatureConverter
      properties:
        relation_id: !variable osm_id

- type: GeoJSONFormatter

- type: OsmoscopeLayerFormatter
  data_format_url: geojson_url
  name: No admin level
  updates: Every evening
  doc:
    description: Every relation with boundary=administrative should have an admin_level value set.
    why_problem: Check https://wiki.openstreetmap.org/wiki/Tag%3Aboundary%3Dadministrative for more information.
    how_to_fix: Add a tag 'admin_level' to the boundary relation.
```

# Syntax

## Overview

Each "section" is called a `Pipe` and must have a `type` defined. The `type`
value must be equal to the name of the pipe's `class`. Available types can
be found in the `nominatim_data_analyser.core.pipes` module.

The `Pipe` definition can then contain others key/values needed for its
good functioning and/or for its configuration.

To get an overview of what `type` of `pipes` exist with a basic explanation of
what they do and their `configuration` and `required fields`,
see the [Main pipes](Pipes.md#Main-pipes) chapter.

Pipes are plugged together in the order they appear in the pipeline list.

## Custom types

Custom types are used in the YAML specification to handle some fields differently. 

### !sub-pipeline

The `!sub-pipeline` type is used to create a field which contains
a sub-pipeline as its content. The `LoopDataProcessor` pipe is a perfect
example for using this custom type:

```yaml
- type: LoopDataProcessor
  sub_pipeline: !sub-pipeline
    - type: GeometryConverter
      geometry_type: Node
    - type: GeoJSONFeatureConverter
```

The value of the `sub_pipeline` field is set to `!sub-pipeline` and then a
pipeline specification is set as its content. By using the `!sub-pipeline`
custom type, the YAML loader knows that it should use the content
of the field to assemble a pipeline. 

Here, the assembled sub-pipeline will be composed of a `GeoJSONFeatureConverter`
pipe plugged to a `GeometryConverter` pipe.

### !variable

The `!variable` type is used to create a value which will be resolved dynamically
at runtime depending on the input data. The variable has a name which will
be looked up in the data dictionary given to resolve this variable in
the python code:

```yaml
address: !variable address
```

Here the YAML Loader will automatically assigns a `Variable` object to the
value of the key `address`. This `Variable` can then be resolved by getting
a data dictionary as input. It will look for the `address` key in this
dictionary and it will return its value.

More explanations on the DynamicValue type can be found in
the [DynamicValue chapter](Dynamic-Value.md).

### !switch

The `!switch` type is used to create a switch condition in the YAML specification.
The switch is a dynamic value which will be resolved at runtime depending on
the data dictionary given to resolve it.

It works the same way as the [switch statement](https://en.wikipedia.org/wiki/Switch_statement)
in many programming languages. If we take the following JavaScript switch
statement as an example:

```javascript
switch(geometryType) {
  case 'N':
    return 'Node';
  case 'W':
    return 'Way';
  case 'R':
    return 'Relation';
}
```

It can be recreated in our YAML Specification like this:

```yaml
- our_value: !switch
    expression: geometryType
    cases:
      'N': Node
      'W': Way
      'R': Relation
```

Here the YAML Loader will automatically assigns a `Switch` object to the
value of the key `our_value`. This `Switch` can then be resolved by getting
a data dictionary as input. It will look for the key equal to the expression
`geometryType`. Then, if the value assigned to this key is for example equal
to `'N'`, the value `Node` will be returned.

More explanations on the DynamicValue type can be found
in the [DynamicValue chapter](Dynamic-Value.md).

# Example explanation

If we get back the YAML Rule specification defined at the beginning of this chapter:

```yaml
---
- type: SQLProcessor
  query: >
    SELECT ST_AsText(centroid) AS geometry_holder, osm_id FROM placex WHERE osm_type='R' AND class='boundary'
    AND type='administrative' AND admin_level >= 15;

- type: LoopDataProcessor
  sub_pipeline: !sub-pipeline
    - type: GeometryConverter
      geometry_type: Node

    - type: GeoJSONFeatureConverter
      properties:
        relation_id: !variable osm_id

- type: GeoJSONFormatter

- type: OsmoscopeLayerFormatter
  data_format_url: geojson_url
  name: No admin level
  updates: Every evening
  doc:
    description: Every relation with boundary=administrative should have an admin_level value set.
    why_problem: Check https://wiki.openstreetmap.org/wiki/Tag%3Aboundary%3Dadministrative for more information.
    how_to_fix: Add a tag 'admin_level' to the boundary relation.
```

We can explain it like that:

* First, a query pipe is defined. This pipe is of type `SQLProcessor`. It
  contains a `query` field which corresponds to the SQL query which will
  be executed by the pipe.
* Next a loop processing pipe is defined. This pipe will be plugged to the
  query pipe. It is of type `LoopDataProcessor` and it contains a
  `sub_pipeline` field which contains the sub-pipeline which will be used by the pipe.
* The `sub-pipeline` contains a `GeoJSONFeatureConverter` pipe which contains
  one property of name 'relation_id' where its value is a `!variable` type of
  name 'osm_id'. At runtime, each record from the `SQL Query` result will
  produce a different value for this variable which will be equal to the
  value of the 'osm_id' field from the `SQL Query`.
* The geojson pipe will be plugged to the loop processing pipe.
  It is of type `GeoJSONFormatter`.
* The layer file pipe will be plugged to the geojson pipe. It is of type
  `OsmoscopeLayerFormatter` and it contains multiples fields used
  as configuration for the layer generation.
