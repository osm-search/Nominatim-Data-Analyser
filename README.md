# Nominatim-Data-Analyser ![CI Build-Tests](https://github.com/osm-search/Nominatim-Data-Analyser/actions/workflows/ci-build-tests.yml/badge.svg)

The Nominatim Data Analyser is a QA tool used to scan the nominatim database and extract
suspect data from it. These data are then presented to mappers through a [visual interface](https://nominatim.org/qa/) so that they can correct them directly.

# Frontend

The repository containing the frontend of the tool can be found [there](https://github.com/osm-search/Nominatim-Data-Analyser-Frontend).

# Installation procedure

## Dependencies

### Code

Clone this repository by running:

```
git clone --recursive https://github.com/osm-search/Nominatim-Data-Analyser
```

### Python

Install python (version 3.5+) and pip.

Install the following python packages:

```
pip install pyyaml geojson wheel psycopg2
```

### Clustering-vt

To set up clustering-vt g++17 minimum is needed:

```
cd clustering-vt/
make
```

## Database

Make sure to have a Nominatim database set up on your server.

The following index has to be created in order for the tool to work:

```
CREATE INDEX IF NOT EXISTS planet_osm_rels_parts_idx ON planet_osm_rels USING gin(parts);
```

You need to run the tool with the nominatim user and/or you should check the database connection settings in ```analyser/database/connection.py```.

## Configuration file

To modify the configuration, you need to copy the ```analyser/config/default.yaml``` to ```analyser/config/config.yaml``` and you can modify the values inside the config.yaml file.

## Frontend set up

To set up the frontend, please check the frontend [repository](https://github.com/osm-search/Nominatim-Data-Analyser-Frontend).

For the webapp to fetch the data extracted by the analyser, you need to serve the ```<RulesFolderPath>``` defined in ```analyser/config/config.yaml``` of the QA Data Analyser Tool with a web server. It should be accessible through the ```<WebPrefixPath>``` also defined in the configuration of the QA Data Analyser Tool.
  
# Running the analyser
  
You can run the tool's analyser with the integrated cli.py:
* --execute-all: Executes all QA rules.
* --filter [rules_names…]: Filters some QA rules so they are not executed.
* --execute-one <rule_name>: Executes the given QA rule.

# Tests

[Pytest](https://docs.pytest.org/en/6.2.x/getting-started.html) is used for the tests and it should be installed:

```
pip install pytest
```

To run the tests for the analyser: execute ```pytest tests/analyser``` command at the root folder of the project.

# Reporting errors in the rule

To report some errors in the rule, please follow the [CONTRIBUTING.md](CONTRIBUTING.md)

# Documentation

An advanced documentation of the tool can be found in the [Overview.md](docs/Overview.md) file.
