import ArrowRightIcon from '../assets/icons/arrow-right.svg';
import ArrowDownIcon from '../assets/icons/arrow-down.svg';
import ReactMarkdown from 'react-markdown';
import { useEffect, useState } from 'react';

/**
 * Map the keys of the layer documentation to a more
 * elaborate value.
 */
const DOC_TITLE_MAPPING = {
    'description': 'Description of the layer',
    'why_problem': 'Why are these data wrong',
    'how_to_fix': 'How to fix these errors'
};

/**
 * Handles one layer item of the main menu. It can be expanded to display the layer's content when clicking on its title.
 * @param {object} props
 * @param {object} props.layerData Data of this layer.
 * @param {object} props.selectedLayer Current selected layer among all the layers.
 * @param {CallableFunction} props.setSelectedLayer Callback to update the state of selectedLayer.
 */
const Layer = ( { layerData, selectedLayer, setSelectedLayer } ) => {
    /**
     * State handling if this layer is opened or closed (its content data are displayed
     * only if its toggle).
     */
    const [isToggle, setToggle] = useState(false);

    /**
     * When the state of selectedLayer change, we should check if the new selectedLayer is
     * equal to the current layer. If it is, we set isToggle to true, otherwise to false.
     */
    useEffect(() => {
        setToggle(selectedLayer && selectedLayer.id === layerData.id)
    }, [selectedLayer])

    /**
     * Generate JSX content of one documentation item based on its key. It is rendered
     * only if the layer is toggle and if the layer data well contains this documentation key.
     * 
     * The key is displayed as the value mapped in DOC_TITLE_MAPPING.
     * @param {string} docKey Key of the documentation item we want to render.
     * @returns JSX content of the documentation item.
     */
    const renderDocElement = (docKey) => {
        if (isToggle && docKey in layerData['doc']) {
            const docTitle = docKey in DOC_TITLE_MAPPING ? DOC_TITLE_MAPPING[docKey] : docKey;
            return (
                <div>              
                    <p className='layer-doc-title'>{docTitle}:</p>
                    <ReactMarkdown className='layer-doc-content' linkTarget='_blank'>{layerData['doc'][docKey]}</ReactMarkdown>
                </div>
            );
        }
        return null;
    }

    return (
        <div className={`layer-wrapper ${isToggle ? 'layer-toggle' : ''}`}>
            <div className='layer-title-arrow-wrapper' onClick={() => setSelectedLayer(isToggle ? null : layerData)}>
                <h3>{layerData.name}</h3>
                <div className="flex-one"></div>
                <img className='layer-arrow-icon' alt='Reset city sort icon' src={isToggle ? ArrowDownIcon : ArrowRightIcon}/>
            </div>
            <div className={`layer-data-wrapper ${isToggle ? 'layer-data-toggle' : ''}`}>
                {renderDocElement('description')}
                {renderDocElement('why_problem')}
                {renderDocElement('how_to_fix')}
            </div>
        </div>
    )
}

export default Layer
