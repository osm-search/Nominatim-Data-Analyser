import './App.css';
import { useState } from 'react'
import MainMenu from './components/MainMenu';
import MapContainer from './components/MapContainer';
import MenuIcon from './assets/icons/menu.svg';
import InformationPanel from './components/InformationPanel';

function App() {
  const [selectedLayer, setSelectedLayer] = useState(null);
  const [isMenuToggle, setMenuToggle] = useState(true);
  const [isInfoPanelDisplayed, setInfoPanelDisplayed] = useState(true);

  return (
    <div className="app">
      <MainMenu isMenuToggle={isMenuToggle} setMenuToggle={setMenuToggle} selectedLayer={selectedLayer} setSelectedLayer={setSelectedLayer}/>
      <MapContainer selectedLayer={selectedLayer}/>
      {
        isInfoPanelDisplayed &&
        <InformationPanel setInfoPanelDisplayed={setInfoPanelDisplayed}/>
      }
      {
        !isMenuToggle &&
        <div className='absolute-menu-icon-wrapper'>
          <img src={MenuIcon} alt='menu icon' className='menu-icon absolute-menu-icon' onClick={() => setMenuToggle(!isMenuToggle)}/>
        </div>
      }
    </div>
  );
}

export default App;
