# Introduction

The Nominatim Data Analyser is a QA tool used to scan the nominatim database and extract
suspect data from it.

Once extracted the data are processed and converted into some output formats like GeoJSON, vector tiles, etc.
The purpose is to use these outputs into other tools like [osmoscope-ui](https://github.com/osmoscope/osmoscope-ui).

When displayed through a public visualization tool, the data can be corrected by mappers directly.

The whole purpose of the Nominatim Data Analyser is to increase the quality of OpenStreetMap data and therefore indirectly the search results of Nominatim.

# Rules

This tool works by executing a set of `rules` where a `rule` is a definition
of what should be done from the data extraction to the outputs generation.

Each rule is defined inside a YAML file following the [YAML Rule Specification](YAML-Rule-Specification.md). This system has been designed in order to provide an easy and visual way of creating a new rule.

All rules can be found in the `analyser/rules_specifications` folder.

To add a new rule follow the [Add a new rule chapter](Add-New-Rule.md).

# Architecture

The tool is designed around a global `Pipeline` architecture where each data processing unit is defined as a class which inherits from the `Pipe` base class. One rule is equal to one pipeline constructed from the YAML Rule file.

The pipeline of a rule is assembled by the `yaml_loader` module. A single 'pipe'
in the pipeline has exactly one input and one output. Some pipes, like
the LoopDataProcessor can be more complex internally and process data through
subpipes but in the end they present exactly one output to the next pipe
element.
