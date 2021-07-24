# Nominatim-Data-Analyser

Analyses the nominatim database to extract wrong OSM data from it.

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
You need to run the tool with the nominatim user and/or you should check the database connection settings in ```analyser/database/connection.py``` (this will be added to configuration file in the future).

# Configuration file

To modify the configuration, you need to copy the ```analyser/config/default.yaml``` to ```analyser/config/config.yaml``` and you can modify the values inside the config.yaml file.

# Osmoscope set up

* Clone [Osmoscope-ui](https://github.com/osmoscope/osmoscope-ui).
* In site/js/app.js modify the line ```load_data_source('http://area.jochentopf.com/osmm/layers.json');``` and replace the url with ```<WebPrefixPath>/layers.json``` where ```<WebPrefixPath>``` is the value defined in the config file of the QA Data Analyser Tool (analyser/config/config.yaml).
* Serve the "site" folder of Omoscope with a web server.
* Serve the ```<RulesFolderPath>``` defined in ```analyser/config/config.yaml``` of the QA Data Analyser Tool with a web server. It should be accessible through the ```<WebPrefixPath>``` also defined in the configuration of the QA Data Analyser Tool.
  
# Tool usage
  
You can use the tool with the integrated cli.py:
* --execute-all: Executes all QA rules.
* --filter [rules_names…]: Filters some QA rules so they are not executed.
* --execute-one <rule_name>: Executes the given QA rule.
