
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

const int maxZoom = 11;

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

        for (int z = 0; z <= maxZoom + 1; z++) {
            const int zoomDimension = std::pow(2, z);
            for (int x = 0; x < zoomDimension; x++) {
                for (int y = 0; y < zoomDimension; y++) {
                    
                    mapbox::feature::feature_collection<std::int16_t> tile = index.getTile(z, x, y);

                    if (tile.size() != 0) {
                        vtzero::tile_builder tileBuilder;
                        vtzero::layer_builder layerBuilder{tileBuilder, "clustersLayer", 1, 256};
                        vtzero::key_index<std::unordered_map> idx{layerBuilder};

                        for (auto &f : tile) {
                            const mapbox::geometry::point<std::int16_t> featurePoint = f.geometry.get<mapbox::geometry::point<std::int16_t>>();

                            {
                                vtzero::point_feature_builder featureBuilder{layerBuilder};
                                featureBuilder.add_point(featurePoint.x, featurePoint.y);
                                properties_to_point_feature_builder {featureBuilder}(f.properties);

                                //Add the clusterExpansionZoom to a property if the feature is a cluster.
                                const auto iterator = f.properties.find("cluster_id");
                                if (iterator != f.properties.end() && iterator->second.get<uint64_t>()) {
                                    uint8_t expansionZoom = index.getClusterExpansionZoom(f.properties["cluster_id"].get<uint64_t>());
                                    featureBuilder.add_property("clusterExpansionZoom", expansionZoom);
                                }

                                featureBuilder.commit();
                            }
                        }

                        const auto data = tileBuilder.serialize();

                        std::ostringstream folderPath;
                        folderPath << argv[1] << "/" << z << "/" << x;

                        std::ostringstream pbfPath;
                        pbfPath << argv[1] << "/" << z << "/" << x << "/" << y << ".pbf";

                        std::filesystem::create_directories(folderPath.str());
                        write_data_to_file(data, pbfPath.str());
                    }
                }
            }
        }

        timer("total tiles generation time");
    }else {
        std::cerr << "GeoJSON is needed in stdin!\n";
        return 1;
    }
}