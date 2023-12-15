import './App.css'
import Map, {Layer, Source} from 'react-map-gl';

function App() {
    return (
        <Map
            mapboxAccessToken={import.meta.env.VITE_MAPBOX_TOKEN}
            initialViewState={{
                longitude: -85.5793,
                latitude: 44.7414,
                zoom: 10
            }}
            style={{width: "100vw", height: "100vh"}}
            mapStyle="mapbox://styles/mapbox/satellite-v9"
        >
            <Source type="raster" tiles={["http://localhost:8000/{z}/{x}/{y}.png"]}>
                <Layer id="raster-layer" type="raster"/>
            </Source>
        </Map>
    )
}

export default App
