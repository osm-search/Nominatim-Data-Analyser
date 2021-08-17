import { Scrollbars } from 'react-custom-scrollbars-2';
import LayersList from "./LayersList"
import GithubIcon from '../assets/icons/github.svg';
import LeftArrowIcon from '../assets/icons/left-arrow.svg';

/**
 * Handles the content of the main menu.
 * @param {object} props
 * @param {boolean} props.isMenuToggle Defines if the menu is toggle or not.
 * @param {CallableFunction} props.setMenuToggle Callback to update the state of isMenuToggle.
 * @param {object} props.selectedLayer Current selected layer among all the layers.
 * @param {CallableFunction} props.setSelectedLayer Callback to update the state of selectedLayer.
 */
const MainMenu = ( { isMenuToggle, setMenuToggle, selectedLayer, setSelectedLayer } ) => {
    return (
        <section className={`main-menu-wrapper ${!isMenuToggle ? 'not-toggle' : ''}`}>
            <div className='menu-title-wrapper'>
                <h1>Nominatim QA</h1>
                <div className='flex-one'></div>
                <img src={LeftArrowIcon} alt='menu icon' className='menu-icon' onClick={() => setMenuToggle(!isMenuToggle)}/>
            </div>
            <p className='layers-label'>Layers:</p>
            <Scrollbars autoHeight autoHeightMax={'100%'}>
                <LayersList selectedLayer={selectedLayer} setSelectedLayer={setSelectedLayer}/>
            </Scrollbars>
            <div className='flex-one'></div>
            <div className='github-wrapper'>
                <img src={GithubIcon} alt='github icon'/>
                <a href='https://github.com/AntoJvlt/Nominatim-Data-Analyser' target='_blank' rel="noreferrer">osm-search/Nominatim-Data-Analyser</a>
            </div>
        </section>
    )
}

export default MainMenu
