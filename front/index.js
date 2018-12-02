import Map from 'ol/Map.js';
import View from 'ol/View.js';
import {
    easeIn,
    easeOut
} from 'ol/easing.js';
import TileLayer from 'ol/layer/Tile.js';
import Overlay from 'ol/Overlay.js';
import {
    platformModifierKeyOnly
} from 'ol/events/condition.js';

import {
    fromLonLat,
    toLonLat
} from 'ol/proj.js';
import OSM from 'ol/source/OSM.js';
import BingMaps from 'ol/source/BingMaps.js';
import {
    Draw,
    Modify,
    Snap
} from 'ol/interaction.js';
import Polygon from 'ol/geom/Polygon';
import {
    Circle,
    Fill,
    Stroke,
    Style
} from 'ol/style.js';
import VectorSource from 'ol/source/Vector';
import VectorLayer from 'ol/layer/Vector.js';




var localFarmingLand = fromLonLat([8.457220, 49.498287]);


var key = 'ArQHbdIiR4xfNFxF-lFdIAKmajD-xKOgzEvelSUSnjT7uaszETzmFJKkilxr53CE';

var roads = new TileLayer({
    source: new BingMaps({
        key: key,
        imagerySet: 'Road'
    })
});
var imagery = new TileLayer({
    source: new BingMaps({
        key: key,
        imagerySet: 'Aerial'
    })
});
var vectorSource = new VectorSource({});
var features = new VectorLayer({
    source: vectorSource
})
var drawingSource = new VectorSource({
    useSpatialIndex: false
});
var drawingLayer = new VectorLayer({
    source: drawingSource
});

var marker1 = new Overlay({
    position: fromLonLat([8.588285, 49.499092]),
    element: document.getElementById('marker1')
});
var marker1 = new Overlay({
    position: fromLonLat([8.585744, 49.494261]),
    element: document.getElementById('marker2')
});





var container = document.getElementById('map');
var myView = new View({
    center: fromLonLat([0, 0]),
    zoom: 1.5
});
var map = new Map({
    layers: [roads, imagery, features],
    target: container,
    view: myView
});
//map.addOverlay(marker1);
//map.addOverlay(marker2);

myView.center = localFarmingLand;
map.addLayer(drawingLayer);
var draw;
// Drawing interaction
draw = new Draw({
    source: drawingSource,
    type: 'Polygon',
    //only draw when Ctrl is pressed.
    condition: platformModifierKeyOnly
});


function onClick(id, callback) {
    document.getElementById(id).addEventListener('click', callback);
}

function onSubmit(id, callback) {
    document.getElementById(id).addEventListener('submit', callback);
}


onClick('rotate-around-localFarmingLand', function () {
    // Rotation animation takes the shortest arc, so animate in two parts
    var rotation = myView.getRotation();
    myView.animate({
        center: localFarmingLand,
        rotation: rotation + Math.PI,
        anchor: localFarmingLand,
        easing: easeIn
    }, {
        rotation: rotation + 2 * Math.PI,
        anchor: localFarmingLand,
        easing: easeOut
    });
    myView.animate({
        center: localFarmingLand,
        zoom: 19,
        duration: 4000
    });

});
onClick('new-farming-area', function () {
    document.getElementById('area-input').className = "input-on";
});
onClick('input', function () {
    document.getElementById('input').value = "[ , ]";
});

var input = document.getElementById('input');
input.addEventListener('keyup', function (e) {
    var code = (e.keyCode ? e.keyCode : 0);
    if (code == 13) { //Enter keycode
        myView.animate({
            zoom: 11,
            center: fromLonLat([8.592858, 49.493398]),
            duration: 4000
        });
        document.getElementById('draw-field').className = "btn btn-primary btn-block draw-field-on";
        document.getElementById('initialWeather').className = "btn btn-primary btn-block draw-field-on";
        document.getElementById('improvedWeather').className = "btn btn-primary btn-block draw-field-on";

        map.addInteraction(draw);

    }
});