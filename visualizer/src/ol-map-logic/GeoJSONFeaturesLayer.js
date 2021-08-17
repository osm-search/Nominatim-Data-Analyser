import SourceVector from 'ol/source/Vector';
import { Vector as VectorLayer } from 'ol/layer';
import GeoJSON from 'ol/format/GeoJSON';
import {Cluster} from 'ol/source';
import ClusteredFeaturesLayer from './ClusteredFeaturesLayer';
import {createEmpty, extend, getCenter} from 'ol/extent';

/**
 * Handles the logic for a features layer with a GeoJSON source.
 */
class GeoJSONFeaturesLayer extends ClusteredFeaturesLayer {
    constructor(layerDefinition) {
        const getFeatureSize = (feature) => feature.get('features').length;
        super(8, 25, getFeatureSize);
        this.source_url = 'geojson_url' in layerDefinition ? layerDefinition['geojson_url'] : '';
    }

    /**
     * Construct the OpenLayers layer with the right informations and with a geojson source.
     * The current date is added to the source_url in order to avoid caching by
     * the browser or server.
     */
    get olLayer() {
        const layer = new VectorLayer({
            source: new Cluster({
                distance: 80,
                source: new SourceVector({
                    url: this.source_url + '?time='+ new Date().getTime(),
                    format: new GeoJSON()
                }),
            }),
            style: (feature) => this.getStyle(feature)
        });
        return layer;
    }

    /**
     * Called when a feature of this layer has been clicked.
     * If the feature is a cluster, the map's view is zoomed to this
     * feature in order to display its child features.
     * 
     * If the feature is not a cluster, the popup is opened with the well constructed content inside.
     */
    onFeatureClick(feature, coordinates, map, overlay, popup) {
        var originalFeatures = feature.get('features');
        if (originalFeatures.length > 1){
            var extent = new createEmpty();
            originalFeatures.forEach(function(f, index, array){
                extend(extent, f.getGeometry().getExtent());
            });
            var resolution = map.getView().getResolutionForExtent(extent);
            var targetZoom = map.getView().getZoomForResolution(resolution);
            var location = getCenter(extent);
            map.getView().animate({
                center: location,
                zoom: targetZoom,
                duration: 1000
            })
        }else {
            popup.current.innerHTML = this.constructPopupContent(feature);
            overlay.setPosition(coordinates); 
        }
    }

    /**
     * Returns the properties of the given feature object.
     */
    getFeatureProperties(feature) {
        return feature.get('features')[0].getProperties();
    }
}

export default GeoJSONFeaturesLayer;