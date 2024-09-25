# Nominatim-Data-Analyser ![CI Build-Tests](https://github.com/osm-search/Nominatim-Data-Analyser/actions/workflows/ci-build-tests.yml/badge.svg)

The Nominatim Data Analyser is a QA tool used to scan the nominatim database and extract
suspect data from it. These data are then presented to mappers through a [visual interface](https://nominatim.org/qa/) so that they can correct them directly.

# Frontend

The repository containing the frontend of the tool can be found [there](https://github.com/osm-search/Nominatim-Data-Analyser-Frontend).

# Installation procedure

Clone this repository by running:

```
git clone https://github.com/osm-search/Nominatim-Data-Analyser
```

Then you can compile everything with

    python3 setup.py build

Or you can directly compile and install the analyser with

    pip install .

## Database

Make sure to have a Nominatim database set up on your server. You can change
the database DSN by supplying a custom config.yaml file.

## Configuration file

To modify the configuration, you need to copy the ```analyser/config/default.yaml``` to ```analyser/config/config.yaml``` and you can modify the values inside the config.yaml file.

## Frontend set up

To set up the frontend, please check the frontend [repository](https://github.com/osm-search/Nominatim-Data-Analyser-Frontend).

For the webapp to fetch the data extracted by the analyser, you need to serve the ```<RulesFolderPath>``` defined in ```analyser/config/config.yaml``` of the QA Data Analyser Tool with a web server. It should be accessible through the ```<WebPrefixPath>``` also defined in the configuration of the QA Data Analyser Tool.
  
# Running the analyser

Analysis is run with the nominatim-data-analyser tool:

* --execute-all: Executes all QA rules.
* --filter [rules_names…]: Filters some QA rules so they are not executed.
* --execute-one <rule_name>: Executes the given QA rule.

During development you can run the same tool directly from the source tree
after having built everything using the supplied `cli.py`.

# Tests

[Pytest](https://docs.pytest.org/en/6.2.x/getting-started.html) is used for the tests and it should be installed:

```
pip install pytest
```

To run the tests for the analyser: execute ```pytest``` command at the root folder of the project.

# Reporting errors in the rule

To report some errors in the rule, please follow the [CONTRIBUTING.md](CONTRIBUTING.md)

# Documentation

An advanced documentation of the tool can be found in the [Overview.md](docs/Overview.md) file.
