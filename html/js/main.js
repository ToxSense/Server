// initialize Leaflet
var map = L.map('map').setView({lon: 9.17, lat: 48.77}, 13);

// add the OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; <a href="https://openstreetmap.org/copyright" target="_blank">OpenStreetMap contributors</a> | &copy; <a href="https://sensor.community" target="_blank">Sensor Data from sensor.community</a> | &copy; <a href="legal.htm">AI Data from ToxSense</a> | <a href="legal.htm">Imprint</a>',
}).addTo(map);

// show the scale bar on the lower left corner
L.control.scale().addTo(map);

var loadIcon = new L.Icon({
  iconUrl: '/img/loading.gif',
  iconAnchor: new L.Point(16, 16),
  iconSize: new L.Point(32, 32),
  size: new L.Point(32, 32),
});

map.on('click', function(data){
  var lat = data.latlng.lat;
  var lon = data.latlng.lng;
  var loadingMarker = L.marker([lat, lon], {'icon':loadIcon,}).addTo(map);
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
     console.log(xhttp.responseText);
     var aqiDict = JSON.parse(xhttp.responseText);
     var aqi = aqiDict['selfaqi'];
     var aqiN = aqi / 300;
     var srcNo = aqiDict['source'];
     var source = '<a href="legal.htm">ToxSense Server-AI</a>';
     if (srcNo == 3){
       var source = '<a href="legal.htm">Interpolated value (less accurate) // TF-Error</a>';
     };
     map.removeLayer(loadingMarker);
     L.circleMarker([lat, lon],{renderer:aqiCanvas,color:'#3dbb7a',}).bindPopup(`AQI: ${aqi}<br />Source: ${source}`).addTo(aqiMarkers);
     heatmapLayer.addData({'lng': lon, 'lat': lat, 'value': aqiN});
    };
  };
  xhttp.open("POST", "https://api.toxsense.de/", true);
  xhttp.setRequestHeader("accept", "application/json");
  xhttp.setRequestHeader("Content-Type", "application/json");
  xhttp.send(`{"lat":${lat},"lon":${lon}}`); 
})


//add heatmap

var cfg = {
    // radius should be small ONLY if scaleRadius is true (or small radius is intended)
    // if scaleRadius is false it will be the constant radius used in pixels
    "radius": 50,
    "maxOpacity": .8,
    "minOpacity": .1,
    // scales the radius based on map zoom
    "scaleRadius": false,
    // if set to false the heatmap uses the global maximum for colorization
    // if activated: uses the data maximum within the current map boundaries
    //   (there will always be a red spot with useLocalExtremas true)
    "useLocalExtrema": false,
    // which field name in your data represents the latitude - default "lat"
    latField: 'lat',
    // which field name in your data represents the longitude - default "lng"
    lngField: 'lng',
    // which field name in your data represents the data value - default "value"
    valueField: 'aqi',
    gradient: {'.083':'darkgreen','0.25':'yellow','0.417':'orange','.583':'red','.833':'purple','1.0':'maroon'}
};
  
  
var heatmapLayer = new HeatmapOverlay(cfg);
heatmapLayer.addTo(map);
heatmapLayer.setData(aqiData);