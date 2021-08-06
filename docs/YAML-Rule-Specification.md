# YAML Rule Specification

A rule is defined inside a YAML Rule file. This file follows the YAML Rule Specification defined in this chapter.

# Introduction

The YAML Rule Specification follows a tree structure and a pipeline architecture (See [Architecture](Overview.md#architecture)). Hence, a specific format should be followed for the rule to work.

For example, here is the YAML Rule Specification for the rule `boundary=administrative without an admin_level value set`:

```yaml
---
QUERY:
  type: SQLProcessor
  query: >
    SELECT ST_AsText(centroid) AS geometry_holder, osm_id FROM placex WHERE osm_type='R' AND class='boundary'
    AND type='administrative' AND admin_level >= 15;
  out:
    LOOP_PROCESSING:
      type: LoopDataProcessor
      sub_pipeline: !sub-pipeline
        GEOMETRY_CONVERTER:
          type: GeometryConverter
          geometry_type: Node
          out:
            FEATURE_CONVERTER:
              type: GeoJSONFeatureConverter
              properties:
                relation_id: $osm_id
      out:
        GEOJSON:
          type: GeoJSONFormatter
          out:
            LAYER_FILE:
              type: OsmoscopeLayerFormatter
              data_format_url: geojson_url
              name: no admin level
              updates: Every evening
              doc:
                description: Every relation with boundary=administrative should have an admin_level value set.
                why_problem: Check https://wiki.openstreetmap.org/wiki/Tag%3Aboundary%3Dadministrative for more informations.
                how_to_fix: Add a tag 'admin_level' to the boundary relation.
```

# Syntax

## Overview

Each "section" is called a `Pipe` and it should have a name. The name has no importance but it should be meaningful and in uppercase (for convention). In the introduction example, the first `Pipe` is called `QUERY`.

Each `Pipe` should have a `type` defined. The `type` value should be equal to the name of the pipe's `class`. It will be used by the `Assembler` to know which class to instantiate for this pipe (See [Architecture](Overview.md#architecture)).

The `Pipe` definition can then contain others key/values needed for its good functioning and/or for its configuration.

To get an overview of what `type` of `pipes` exist with a basic explanation of what they do and their `configuration` and `required fields`, see the [Main pipes](Pipes.md#Main-pipes) chapter.

The `out` field is used to specify which pipes to plug to the current pipe. This field contains the definition of the pipes to plug to the current pipe. It can contain multiples pipes and not only one, just like this example:

```yaml
---
QUERY:
  type: SQLProcessor
  query: >
    DUMB_QUERY
  out:
    FEATURE_CONVERTER:
        type: GeoJSONFeatureConverter
        properties:
        relation_id: $osm_id
    GEOJSON:
        type: GeoJSONFormatter
```

The `FEATURE_CONVERTER` and `GEOJSON` pipes are both plugged to the `QUERY` pipe.

## Custom types

Custom types are used in the YAML specification to handle some fields differently. 

### !sub-pipeline

The `!sub-pipeline` type is used to create a field which contains a sub-pipeline as its content. The `LoopDataProcessor` pipe is a perfect example for using this custom type:

```yaml
LOOP_PROCESSING:
  type: LoopDataProcessor
  sub_pipeline: !sub-pipeline
    GEOMETRY_CONVERTER:
      type: GeometryConverter
      geometry_type: Node
      out:
        FEATURE_CONVERTER:
          type: GeoJSONFeatureConverter
          properties:
            relation_id: $osm_id
```

The value of the `sub_pipeline` field is set to `!sub-pipeline` and then a pipeline specification is set as its content. By using the `!sub-pipeline` custom type, the YAML loader knows that it should use the content of the field to assemble a pipeline. 

Here, the assembled sub-pipeline will be composed of a `GeoJSONFeatureConverter` pipe plugged to a `GeometryConverter` pipe.

# Example explanation

If we get back the YAML Rule specification defined at the beggining of this chapter:

```yaml
---
QUERY:
  type: SQLProcessor
  query: >
    SELECT ST_AsText(centroid) AS geometry_holder, osm_id FROM placex WHERE osm_type='R' AND class='boundary'
    AND type='administrative' AND admin_level >= 15;
  out:
    LOOP_PROCESSING:
      type: LoopDataProcessor
      sub_pipeline: !sub-pipeline
        GEOMETRY_CONVERTER:
          type: GeometryConverter
          geometry_type: Node
          out:
            FEATURE_CONVERTER:
              type: GeoJSONFeatureConverter
              properties:
                relation_id: $osm_id
      out:
        GEOJSON:
          type: GeoJSONFormatter
          out:
            LAYER_FILE:
              type: OsmoscopeLayerFormatter
              data_format_url: geojson_url
              name: no admin level
              updates: Every evening
              doc:
                description: Every relation with boundary=administrative should have an admin_level value set.
                why_problem: Check https://wiki.openstreetmap.org/wiki/Tag%3Aboundary%3Dadministrative for more informations.
                how_to_fix: Add a tag 'admin_level' to the boundary relation.
```

We can explain it like that:

* First, a `QUERY` pipe is defined. This pipe is of type `SQLProcessor`. It contains a `query` field which corresponds to the SQL query wich will be executed by the pipe.

* In the `out` field of the `QUERY` pipe, a `LOOP_PROCESSING` pipe is defined. Hence, this pipe will be plugged to the `QUERY` pipe. It is of type `LoopDataProcessor` and it contains a `sub_pipeline` field which contains the sub-pipeline which will be used by the pipe.

* The pipe `GEOJSON` will be plugged to the `LOOP_PROCESSING` pipe. It is of type `GeoJSONFormatter`.

* The pipe `LAYER_FILE` will be plugged to the `GEOJSON` pipe. It is of type `OsmoscopeLayerFormatter` and it contains multiples fields used as configuration for the layer generation.