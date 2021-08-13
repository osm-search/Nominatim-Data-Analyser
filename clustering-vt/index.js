#! /usr/bin/env node

const { program } = require('commander')
const Supercluster = require('supercluster');
const VTpbf = require('vt-pbf');
const fs = require('fs');

const MAX_ZOOM = 13;

const features = [];

program
    .command('generate <radius> <output_dir>')
    .description('Generates the clusters and creates vector tiles in the given output-dir.')
    .action(generate);
    
function generate(radius, output_dir) {
    if(!features) {
        throw new Error('A FeatureCollection should be sent through stdin.');
    }
    const superCluster = new Supercluster({ radius: radius, maxZoom: MAX_ZOOM, extent: 256});
    console.time('Clusters generation');
    const clusteredFeatures = superCluster.load(features);
    console.timeEnd('Clusters generation');

    //Remove the output directory with its content if it exists.
    fs.rm(output_dir, { recursive: true, force: true }, (rmdir_err) => {
        if (rmdir_err) throw rmdir_err;
        console.time('Vector tiles creation')
        for (let z = 0; z <= MAX_ZOOM + 1; z++) {
            console.log(z)
            const zoomDimension = Math.pow(2, z);
            for (let x = 0; x < zoomDimension; x++) {
                for (let y = 0; y < zoomDimension; y++) {
                    const tile = clusteredFeatures.getTile(z, x, y);

                    //Do not serialize empty tiles.
                    if (!tile || !tile.features) {
                        continue;
                    }

                    var pbfData = VTpbf.fromGeojsonVt({ 'geojsonLayer': tile }, { extent: 256 });

                    fs.mkdir(`${output_dir}/${z}/${x}`, { recursive: true }, (mkdir_err) => {
                        if (mkdir_err) throw mkdir_err;
                        fs.writeFileSync(`${output_dir}/${z}/${x}/${y}.pbf`, pbfData);
                    });
                }
            }
        }
        console.timeEnd('Vector tiles creation')
    });
}

// Read data from stdin before parsing the args
if(process.stdin.isTTY) {
    program.parse(process.argv);
} else {
    var currentBuffer = "";
    var startParsing = false;
    process.stdin.on('readable', function() {
        var chunk = this.read(); 

        if (chunk !== null) {
            chunk.forEach(element => {
                currentBuffer += String.fromCharCode(element);
                //Ignore the beggining of the FeatureCollection
                if (currentBuffer.endsWith('"features": [')) {
                    currentBuffer = "";
                    startParsing = true;
                }
                if (startParsing) {
                    //Check that we reached a new Feature
                    if (currentBuffer.endsWith('{"type": "Feature"')) {
                        //Check that this is not the first Feature
                        if(currentBuffer.length > 18) {
                            const strFeatureToParse = currentBuffer.slice(0, -20); // remove the last part = ,{"type": "Feature"
                            currentBuffer = currentBuffer.slice(-18); //Keep only {"type": "Feature"
                            feature = JSON.parse(strFeatureToParse);
                            features.push(feature);
                            if (features.length % 5000 == 0) {                       
                                console.log(features.length);
                            }
                        }
                    }
                }
            });
        }
    });
    process.stdin.on('end', function() {
        program.parse(process.argv); 
    });
}