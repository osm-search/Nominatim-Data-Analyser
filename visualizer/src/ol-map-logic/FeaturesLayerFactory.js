import GeoJSONFeaturesLayer from "./GeoJSONFeaturesLayer";
import VectorTileFeaturesLayer from "./VectorTileFeaturesLayer";

/**
 * Factory to create the right features layers based on the layer definition.
 */
class FeaturesLayerFactory {
    static constructFeaturesLayer(layerDefinition) {
        if ('geojson_url' in layerDefinition) {
            return new GeoJSONFeaturesLayer(layerDefinition)
        }else if ('vector_tile_url') {
            return new VectorTileFeaturesLayer(layerDefinition);
        }else {
            return null;
        }
    }
}

export default FeaturesLayerFactory;