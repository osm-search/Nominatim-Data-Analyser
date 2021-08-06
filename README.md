# Nominatim-Data-Analyser

The Nominatim Data Analyser is a QA tool used to scan the nominatim database and extract
suspect data from it. These data are then presented to mappers through a visual interface so that they can correct them directly.

The advanced documentation of this tool can be found there: [docs/Overview.md](docs/Overview.md).

# Installation procedure

### Dependencies

Install python (version 3.5+) and pip.

Install the following python packages:

```
pip install pyyaml geojson wheel psycopg2
```

You need [Tippecanoe](https://github.com/mapbox/tippecanoe) to be installed on your server. Installation instructions can be found [there](https://github.com/mapbox/tippecanoe#installation).

### Database

Make sure to have a Nominatim database set up on your server.

The following index has to be created in order for the tool to work:

```
CREATE INDEX IF NOT EXISTS planet_osm_rels_parts_idx ON planet_osm_rels USING gin(parts);
```

You need to run the tool with the nominatim user and/or you should check the database connection settings in ```analyser/database/connection.py``` (this will be added to configuration file in the future).

# Configuration file

To modify the configuration, you need to copy the ```analyser/config/default.yaml``` to ```analyser/config/config.yaml``` and you can modify the values inside the config.yaml file.

# Osmoscope set up

* Clone [Osmoscope-ui](https://github.com/osmoscope/osmoscope-ui).
* In site/js/app.js modify the line ```load_data_source('http://area.jochentopf.com/osmm/layers.json');``` and replace the url with ```<WebPrefixPath>/layers.json``` where ```<WebPrefixPath>``` is the value defined in the config file of the QA Data Analyser Tool (analyser/config/config.yaml).
* Serve the "site" folder of Osmoscope with a web server.
* Serve the ```<RulesFolderPath>``` defined in ```analyser/config/config.yaml``` of the QA Data Analyser Tool with a web server. It should be accessible through the ```<WebPrefixPath>``` also defined in the configuration of the QA Data Analyser Tool.
  
# Tool usage
  
You can use the tool with the integrated cli.py:
* --execute-all: Executes all QA rules.
* --filter [rules_names…]: Filters some QA rules so they are not executed.
* --execute-one <rule_name>: Executes the given QA rule.

# Tests

[Pytest](https://docs.pytest.org/en/6.2.x/getting-started.html) is used for the tests and it should be installed:

```
pip install pytest
```

To run the tests: execute the ```pytest``` command inside the /tests folder of the project.
