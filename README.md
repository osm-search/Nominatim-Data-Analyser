# Nominatim-Data-Analyser ![CI Build-Tests](https://github.com/AntoJvlt/Nominatim-Data-Analyser/actions/workflows/ci-build-tests.yml/badge.svg)

The Nominatim Data Analyser is a QA tool used to scan the nominatim database and extract
suspect data from it. These data are then presented to mappers through a visual interface so that they can correct them directly.

# Modules available

The Nominatim Data Analyser is runned by 3 modules:

* The ```analyser/``` module is the main module written in python which analyses the Nominatim database to extract the wrong data from it based on some QA rules. An advanced documentation of this module can be found there: [docs/Overview.md](docs/analyser/Overview.md).
* The ```clustering-vt/``` module is a custom tool written in Javascript. It runs on the server with [Node.js](https://nodejs.org/en/) and it is needed by the ```analyser/``` to work. This module generates clusters from a set of data features with the help of [Supercluster](https://github.com/mapbox/supercluster) and it generates vector tiles which can be consumed by the frontend with the help of [vt-pbf](https://github.com/mapbox/vt-pbf).
* The ```visualizer/``` module is a [React](https://reactjs.org/) web app which is used as the frontend of the Nominatim Data Analyser to visualize the extracted data and to allow mappers to correct them.

# Installation procedure

## Dependencies

Install python (version 3.5+) and pip.

Install the following python packages:

```
pip install pyyaml geojson wheel psycopg2
```

You need [Tippecanoe](https://github.com/mapbox/tippecanoe) to be installed on your server. Installation instructions can be found [there](https://github.com/mapbox/tippecanoe#installation).

[Node.js](https://nodejs.org/en/) (version 12.10+) should be installed on the server which runs the analyser. It is also needed to build the frontend. To get the right package for your distribution you can check the [Node.js Binary Distribution repository](https://github.com/nodesource/distributions).

## Database

Make sure to have a Nominatim database set up on your server.

The following index has to be created in order for the tool to work:

```
CREATE INDEX IF NOT EXISTS planet_osm_rels_parts_idx ON planet_osm_rels USING gin(parts);
```

You need to run the tool with the nominatim user and/or you should check the database connection settings in ```analyser/database/connection.py```.

## Clustering-vt

Clustering-vt needs to be built in order for the tool to work. You need [Node.js](https://nodejs.org/en/) to run clustering-vt as explained previously in the dependencies section.

Go into the ```clustering-vt/``` folder and run:

```
npm install
```
This will install all the dependencies required for this module. Then run:

```
npm install clustering-vt -g
```

To install clustering-vt globally on the server.

## Configuration file

To modify the configuration, you need to copy the ```analyser/config/default.yaml``` to ```analyser/config/config.yaml``` and you can modify the values inside the config.yaml file.

## Frontend set up

The React frontend app can be found in the ```visualizer/``` folder. Before building it you need to change some parameters:

* In the ```visualizer/src/config/config.json``` file you need to set the right ```WEB_PATH``` which is the URL defined as the ```WebPrefixPath``` value in the config file of the analyser (analyser/config/config.yaml). This is needed to fetch the data files from the server.

* If you will serve this frontend on a specific path like ```https://your-server.org/Nominatim-QA-Frontend``` you need to add ```"homepage": "https://your-server.org/Nominatim-QA-Frontend"``` in the package.json file inside the visualizer/ folder. This line can be added under ```"private": true``` for example.
By doing that, the app will add the prefix Nominatim-QA-Frontend/ before all its requests to static files when it gets built.
If you will serve the app at the root url of your server this step is not needed.

To build the app go into the ```visualizer/``` folder and run:
```
npm install
```
This will install all the dependencies required by the app and then run:
```
npm run build
```
Then you need to serve the ```visualizer/build``` folder with any webserver to access the app.

For the app to fetch the data extracted by the analyser, you need to serve the ```<RulesFolderPath>``` defined in ```analyser/config/config.yaml``` of the QA Data Analyser Tool with a web server. It should be accessible through the ```<WebPrefixPath>``` also defined in the configuration of the QA Data Analyser Tool.
  
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