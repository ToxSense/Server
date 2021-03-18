<?php

# FUNCTIONS
function cleanb64($string) {
	return preg_replace('/[^a-zA-Z+/=]/', '', $string); // Removes non b64 chars.
};


# MAIN SCRIPT
if (isset($_GET['request'])){
	$request = cleanb64($_GET['request']);

	/* ob_start();
	passthru('/usr/bin/python3 '.dirname(__FILE__).'/request.py '.$request);
	$output = ob_get_clean();
	echo $output; */
} else {
?>
<!DOCTYPE HTML>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>ToxSense</title>
    <meta name="description" content="Website of the ToxSense-Project">
    <meta name="author" content="Timo Bilhöfer">
    <link rel="icon" type="image/png" href="img/logo.png">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <link rel="stylesheet" href="js/leaflet/leaflet.css" integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A==" crossorigin="" />
    <link rel="stylesheet" href="css/styles.css" />
  </head>
  <body>
    <header>
      <img src="img/logo.png" alt="ToxSense Logo" id="logo"/>
      <h1>To<span class="green">x</span>Sense <span class="grey">Map</span></h1>
    </header>
    <div id="map"></div>

    <script>
    <?php
      //init Heatmap
      echo "var aqiData = {min:0,max:1, data: [";
      //get data from db
      $servername = $_SERVER['MYSQL_HOST'];
      $username = $_SERVER['MYSQL_USER'];
      $password = $_SERVER['MYSQL_PASSWORD'];
      $db = $_SERVER['MYSQL_DATABASE'];

      $conn = new mysqli($servername, $username, $password, $db);
      if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
      } 
      $sql = "SELECT lat, lon, aqi, source FROM toxsense";
      $result = $conn->query($sql);

      if ($result == false) {
        die("Connection failed: No Data");
      }
      
      $markers = "";

      //write data into array
      while($row = $result->fetch_assoc()) {
        $aqi = $row['aqi'];
        $aqiN = $row['aqi'] / 300;
        $lat = $row['lat'];
        $lon = $row['lon'];
        switch ($row['source']) {
          case 0:
            $source = '<a href="legal.htm">ToxSense Headband-AI</a>';
            break;
          case 1:
            $source = '<a href="https://sensor.community" target="_blank">sensor.community</a>';
            break;
          case 2:
            $source = '<a href="legal.htm">ToxSense Server-AI</a>';
            break;
          case 2:
            $source = '<a href="legal.htm">Interpolated value (less accurate) // TF-Error</a>';
            break;
          default:
            $source = 'N.A.';
            break;
        }
        echo "{lat: " . $row['lat'] . ", lng: " . $row['lon'] . ", aqi: " . $aqiN+0.00001 . "},";
        //also make aqimarker script for later generation
        $markers .= "aqiMarkers.addLayer(L.circleMarker([$lat, $lon],{renderer:aqiCanvas,color:'#3dbb7a',}).bindPopup('AQI: $aqi<br />Source: $source'));";
      }

      //finish Heatmap init
      echo "]};";

      //init Markers
      
    ?>
    </script>
    <script src="js/leaflet/leaflet.js" integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA==" crossorigin=""></script>
    <script src="js/heatmap.wip.js"></script>
    <script src="js/leaflet-heatmap.js"></script>
    <script src="js/main.js"></script>
    <script>
      var aqiCanvas = L.canvas({ padding: 0.5 });
      var aqiMarkers = new L.FeatureGroup();
      <?php echo $markers ?>
      map.on('zoomend', function() {
        if (map.getZoom() < 15){
          map.removeLayer(aqiMarkers);
        }
        else {
          map.addLayer(aqiMarkers);
        }
      });
    </script>
    
  </body>
</html>
<?php
};

?>
