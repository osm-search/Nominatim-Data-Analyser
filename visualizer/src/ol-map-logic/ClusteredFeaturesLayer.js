import { Style, Circle, Stroke, Fill, Text, Icon } from "ol/style";
import LocationPin from '../assets/icons/location-pin.svg';

/**
 * Filter containing all the keys which should be ignored when
 * the properties of a feature are rendered.
 */
const FILTERED_PROPERTY_KEYS = [
    'geometry',
    'layer'
]

/**
 * Class handling the logic of a clustered features layer.
 */
class ClusteredFeaturesLayer {
    constructor(mediumSize, bigSize, getFeatureSize) {
        this.mediumSize = mediumSize;
        this.bigSize = bigSize;
        this.getFeatureSize = getFeatureSize;
        this.textFill = new Fill({color: '#fff'});
        this.greenFill = new Fill({color:"rgba(0,128,0,1)"});
        this.orangeFill = new Fill({color:"rgba(255,128,0,1)"});
        this.redFill = new Fill({color:"rgba(192,0,0,1)"});
        this.singleIconStyle = new Style({
            image: new Icon({
                src: LocationPin,
                scale: 1.2
              }),
        });
        this.styleCache = {};
    }

    /**
     * Returns a Fill object different based on the size given in parameter. This function is needed
     * to not recreate a Fill object whenever we render a feature.
     * @param {number} size Size of the feature.
     * @returns {Fill} OpenLayers Fill object corresponding to the size. 
     */
    getFillBySize(size) {
        return size>this.bigSize ? this.redFill : size>this.mediumSize ? this.orangeFill : this.greenFill;
    }

    /**
     * Generate the OpenLayers Style for the given feature. The style is dynamically
     * generated based on the clustered feature size and other parameters.
     * @returns {Style} OpenLayers style of the feature.
     */
    getStyle(feature){
        var size = this.getFeatureSize(feature);
        var style = this.styleCache[size];
        if (!style) {
            if (size === 1) {
                style = this.styleCache[size] = this.singleIconStyle;
            }else {
                const color = size>this.bigSize ? '192,0,0' : size>this.mediumSize ? '255,128,0' : '0,128,0';
                var radius = Math.max(8, Math.min(size*0.15, 20));
                var dash = 2*Math.PI*radius/6;
                var dash = [ 0, dash, dash, dash, dash, dash, dash ];
                style = this.styleCache[size] = new Style({
                    image: new Circle({
                        radius: radius,
                        stroke: new Stroke({
                        color: "rgba("+color+",0.5)", 
                        width: 15 ,
                        lineDash: dash,
                        lineCap: "butt"
                        }),
                        fill: this.getFillBySize(size)
                    }),
                    text: new Text({
                        text: size.toString(),
                        fill: this.textFill
                    })
                });
            }
        }
        return style;
    }

    /**
     * Called when a feature of this layer has been clicked.
     * This method should be overriden by the child classes.
     */
    onFeatureClick(feature, coordinates, map, overlay, popup) {
        return;
    }

    /**
     * Returns the properties of the given feature object.
     * This method should be overriden by the child classes.
     */
    getFeatureProperties(feature) {
        return {};
    }

    /**
     * Generate the content of the popup. The content is the HTML representation of the
     * features properties.
     * 
     * If the key of the property follows a specific pattern, its value get replaced by a link to
     * the OpenStreetMap matching feature (based on its osm_id).
     * @returns {String} HTML content in String format.
     */
    constructPopupContent(feature) {
        const properties = this.getFeatureProperties(feature);
        const re_numeric = /^[0-9]+$/;
        var out = '';
        
        for (var p in properties) {
            if (properties.hasOwnProperty(p)) {
                var value = properties[p].toString();
                if (FILTERED_PROPERTY_KEYS.includes(p)) {
                    continue;
                } else if ((p === 'node_id' || p === 'way_id' || p === 'relation_id' || p.match('^[nwr]\/@id')) && value.match(re_numeric)) {
                    //Get the data type ('n' or 'w' or 'r')
                    const data_type = p.charAt(0)
                    if (p.match('^[nwr]\/@id')) {
                        p = p.slice(5)
                    } else {
                        //For example transform 'node_id' into 'Node ID'
                        const splitted = p.split('_')
                        p = splitted[0].charAt(0).toUpperCase() + splitted[0].slice(1) + ' ' + splitted[1].toUpperCase()
                    }
                    const types_mapping = {
                        n: 'node',
                        w: 'way',
                        r: 'relation'
                    }
                    value = '<a target="_blank" href="https://www.openstreetmap.org/' + types_mapping[data_type] + '/' + value + '">' + value + '</a>';
                } else if (p === 'timestamp') {
                    p = 'Timestamp';
                    value = value.replace(/^([0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9])T([0-9][0-9]:[0-9][0-9]:[0-9][0-9])Z$/, "$1 $2");
                }
                out += `<p><span class='bold'>${p}</span>: ${value}</p>`;
            }
        }
        return out;
    }
}

export default ClusteredFeaturesLayer;