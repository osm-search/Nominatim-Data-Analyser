
#include <mapbox/geojson.hpp>
#include <mapbox/geojson_impl.hpp>
#include <rapidjson/document.h>
#include "rapidjson/istreamwrapper.h"
#include <vtzero/builder.hpp>
#include <vtzero/index.hpp>

#define DEBUG_TIMER false

#include <supercluster.hpp>

#include <iostream>
#include <fstream>
#include <string>
#include <iterator>
#include <filesystem>

const int maxZoom = 13;

int amountRemoved = 0;
int amountCreated = 0;

struct properties_to_point_feature_builder {
    vtzero::point_feature_builder& featureBuilder;
    std::string key = "";

    void operator()(mapbox::feature::null_value_t) {
        featureBuilder.add_property(key, NULL);
    }

    void operator()(bool val) {
        featureBuilder.add_property(key, val);
    }

    void operator()(int64_t val) {
        featureBuilder.add_property(key, val);
    }

    void operator()(uint64_t val) {
        featureBuilder.add_property(key, val);
    }

    void operator()(double val) {
        featureBuilder.add_property(key, val);
    }

    void operator()(const std::string& val) {
        featureBuilder.add_property(key, val);
    }

    void operator()(const std::vector<mapbox::feature::value>& array) {
        return;
    }

    void operator()(const std::unordered_map<std::string, mapbox::feature::value>& map) {
        for (const auto& property : map) {
            key.assign(property.first.data());
            mapbox::feature::value::visit(property.second, *this);
        }
    }
};

void write_data_to_file(const std::string& buffer, const std::string& filename) {
    std::ofstream stream{filename, std::ios_base::out | std::ios_base::binary};
    if (!stream) {
        throw std::runtime_error{std::string{"Can not open file '"} + filename + "'"};
    }

    stream.exceptions(std::ifstream::failbit);
    stream.write(buffer.data(), static_cast<std::streamsize>(buffer.size()));

    stream.close();
}

bool try_delete_tile(const std::string& pbfPath) {
    const bool removed = std::filesystem::remove(pbfPath);
    if (removed) {
        amountRemoved++;
    }
    return removed;
}

std::string getTileFolderPath(const std::string& outputFolder, const short zoom, const int x) {
    std::ostringstream folderPathStream;
    folderPathStream << outputFolder << "/" << zoom << "/" << x;
    return folderPathStream.str();
}

std::string getTilePbfPath(const std::string& outputFolder, const short zoom, const int x, const int y) {
    std::ostringstream pbfPathStream;
    pbfPathStream << outputFolder << "/" << zoom << "/" << x << "/" << y << ".pbf";
    return pbfPathStream.str();
}

void delete_sub_tiles(const short zoom, 
                      const int firstTileX, 
                      const int firstTileY, 
                      const std::string& outputFolder) {
    for (int x = firstTileX; x < firstTileX + 2; x++) {
        for (int y = firstTileY; y < firstTileY + 2; y++) {
            const std::string pbfPath = getTilePbfPath(outputFolder, zoom, x, y);

            if (try_delete_tile(pbfPath) && zoom + 1 <= maxZoom + 1) {
                delete_sub_tiles(
                    zoom + 1,
                    2*x, //To understand how we get the subtiles coordinates, check the "subtiles" section: https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
                    2*y,  //We only call the generate_tiles for the subtile in the top left corner of the four subtiles.
                    outputFolder
                );
            }
        }
    }
}

/**
 * Recursively generates all tiles.
 * 
 * The firstTileX and firstTileY parameters are the coordinates of
 * the top left tile of the group of subtiles that we want to generate. 
 * See https://docs.microsoft.com/en-us/bingmaps/articles/bing-maps-tile-system
 * 
 * For each of the four tiles of the group, if a tile contains features and contains at least
 * one cluster, all its child tiles (four tiles again) are generated for the next zoom level 
 * by the same function recursively.
 * 
 * The recursion stop when we read the max zoom level + 1 or if there is no tiles left to generate because
 * there are no clusters left.
 */
void generate_tiles(const short zoom, 
                    const int firstTileX, 
                    const int firstTileY, 
                    const std::string& outputFolder, 
                    mapbox::supercluster::Supercluster& superclusterIndex) {
    for (int x = firstTileX; x < firstTileX + 2; x++) {
        for (int y = firstTileY; y < firstTileY + 2; y++) {
            mapbox::feature::feature_collection<std::int16_t> tile = superclusterIndex.getTile(zoom, x, y);
            
            bool shouldDeleteChildTiles = false;

            const std::string folderPath = getTileFolderPath(outputFolder, zoom, x);
            const std::string pbfPath = getTilePbfPath(outputFolder, zoom, x, y);

            if (tile.size() != 0) {
                vtzero::tile_builder tileBuilder;
                vtzero::layer_builder layerBuilder{tileBuilder, "clustersLayer", 1, 256};
                vtzero::key_index<std::unordered_map> idx{layerBuilder};

                bool hasCluster = false;

                for (auto &f : tile) {
                    const mapbox::geometry::point<std::int16_t> featurePoint = f.geometry.get<mapbox::geometry::point<std::int16_t>>();
                    {
                        vtzero::point_feature_builder featureBuilder{layerBuilder};
                        featureBuilder.add_point(featurePoint.x, featurePoint.y);
                        properties_to_point_feature_builder {featureBuilder}(f.properties);

                        //Add the clusterExpansionZoom to a property if the feature is a cluster.
                        const auto iterator = f.properties.find("cluster_id");
                        if (iterator != f.properties.end() && iterator->second.get<uint64_t>()) {
                            hasCluster = true;
                            uint8_t expansionZoom = superclusterIndex.getClusterExpansionZoom(f.properties["cluster_id"].get<uint64_t>());
                            featureBuilder.add_property("clusterExpansionZoom", expansionZoom);
                        }

                        featureBuilder.commit();
                    }
                }

                const auto data = tileBuilder.serialize();

                std::filesystem::create_directories(folderPath);
                write_data_to_file(data, pbfPath);
                amountCreated++;

                //If there is features and clusters inside the tile, we need to also generate its child tiles.
                //Generate until maxZoom + 1 to also add features where there is no clusters left.
                if (zoom + 1 <= maxZoom + 1) {
                    if (hasCluster) {
                        generate_tiles(
                            zoom + 1,
                            2*x, //To understand how we get the subtiles coordinates, check the "subtiles" section: https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
                            2*y,  //We only call the generate_tiles for the subtile in the top left corner of the four subtiles.
                            outputFolder,
                            superclusterIndex
                        );
                    }else {
                        shouldDeleteChildTiles = true;
                    }
                }
            }else {
                if (try_delete_tile(pbfPath) && zoom + 1 <= maxZoom + 1) {
                    shouldDeleteChildTiles = true;
                }
            }

            if (shouldDeleteChildTiles) {
                delete_sub_tiles(
                    zoom + 1,
                    2*x, //To understand how we get the subtiles coordinates, check the "subtiles" section: https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
                    2*y,  //We only call the generate_tiles for the subtile in the top left corner of the four subtiles.
                    outputFolder
                );
            }

            //At zoom level = 0 there is only 1 one tile, so we should return after it has been generated.
            if (zoom == 0 && firstTileX == 0 && firstTileY == 0) {
                return;
            }
        }
    }
}

int main(int argc, char *argv[]) {
    if (argc == 1) {
        std::cerr << "The output folder is missing!\n";
        return 1;
    }

    if (argc == 2) {
        std::cerr << "The radius is missing!\n";
        return 1;
    }

    //Read GeoJSON data from stdin
    std::cin.sync_with_stdio(false);
    if (std::cin.rdbuf()->in_avail()) {
        
        mapbox::supercluster::Timer timer;

        rapidjson::IStreamWrapper isw(std::cin);
        mapbox::geojson::rapidjson_document d;
        d.ParseStream<rapidjson::IStreamWrapper>(isw);

        timer("parse JSON");

        const auto &json_features = d["features"];

        mapbox::feature::feature_collection<double> features;
        features.reserve(json_features.Size());

        for (auto itr = json_features.Begin(); itr != json_features.End(); ++itr) {
            mapbox::feature::feature<double> feature = mapbox::geojson::convert<mapbox::feature::feature<double>>(*itr);
            features.push_back(feature);
        }
        timer("convert to geometry.hpp");

        mapbox::supercluster::Options options;
        options.maxZoom = maxZoom;
        options.radius = std::atoi(argv[2]);
        options.extent = 256;
        mapbox::supercluster::Supercluster index(features, options);

        timer("total supercluster time");

        generate_tiles(0, 0, 0, argv[1], index);

        timer("total tiles generation time");
        std::cout << "Tiles created: " << amountCreated << "\n";
        std::cout << "Tiles removed: " << amountRemoved << "\n";
    }else {
        std::cerr << "GeoJSON is needed in stdin!\n";
        return 1;
    }
}