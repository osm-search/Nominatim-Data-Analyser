import { trackPromise } from 'react-promise-tracker';
import { useEffect, useState } from 'react';
import config from '../config/config.json';
import Layer from './Layer';
import LoadingIndicator from './LoadingIndicator';

/**
 * Handles the loading and display of all layers.
 * @param {object} props
 * @param {object} props.selectedLayer Current selected layer among all the layers.
 * @param {CallableFunction} props.setSelectedLayer Callback to update the state of selectedLayer.
 */
const LayersList = ( { selectedLayer, setSelectedLayer } ) => {
    /**
     * State which contains all the layers.
     */
    const [layers, setLayers] = useState([]);

    /**
     * Layers are loaded from the server when the component is
     * initialized.
     */
    useEffect(() => {
        loadAndWaitLayers()
    }, [])

    /**
     * Wrapper function needed to track all the promises (with trackPromise()) 
     * executed in loadLayers() at once.
     */
    const loadAndWaitLayers = async () => {
        await trackPromise(loadLayers(), 'layers-fetch');
    }

    /**
     * Load layers.json files from the remote server.
     * For each layer, its data content is loaded from the remove server as well.
     */
    const loadLayers = async () => {
        const requestInit = {
            method: 'GET',
            cache: 'no-cache'
        };
        const layersURL = await (await fetch(`${config.WEB_PATH}/layers.json`, requestInit)).json();
        const loadedLayers = []
        if (layersURL) {
            for (const layerURL of layersURL.layers) {
                const layerData = await (await fetch(layerURL, requestInit)).json()
                //Set the id to an unique id.
                layerData['id'] = layersURL.layers.indexOf(layerURL);
                loadedLayers.push(layerData)
            }
            setLayers(loadedLayers);
        }
    }

    return (
        <div className='layers-list-wrapper'>
            <LoadingIndicator size={60} area='layers-fetch' className='layers-loading-indicator'/>
            {layers.map(layer => <Layer key={layer.id} layerData={layer} selectedLayer={selectedLayer} setSelectedLayer={setSelectedLayer}/>)}
        </div>
    )
}

export default LayersList
