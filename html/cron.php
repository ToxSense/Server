<?php


$ts = time();

$lastCronF = fopen('lastCron.txt', "r");
if (!$lastCronF){
    echo 'first execution!';
} else {
    $lastCron = fgets($lastCronF);
    fclose($lastCronF);
    if ($ts - $lastCron < 900) {
        die('too many executions!');
    }
}

$cronTS = fopen('lastCron.txt', "w");
fwrite($cronTS, $ts);
fclose($cronTS);


include("calcAqi.php");

//DL json from sensor community
$json = file_get_contents("https://maps.sensor.community/data/v2/data.dust.min.json");

if ($json == false){
    die("Connection failed... Could not read json data.");
}

/* $jsonIterator = new RecursiveIteratorIterator(
    new RecursiveArrayIterator(json_decode($json, TRUE)),
    RecursiveIteratorIterator::SELF_FIRST); */

$jsonArray = json_decode($json, TRUE);

$dataArray = array();
$ts = time();
$sql = "";

foreach ($jsonArray as $key) {
    $lat = $key['location']['latitude'];
    $lon = $key['location']['longitude'];
    foreach ($key['sensordatavalues'] as $vals) {
        if ($vals['value_type'] == 'P1') {
            $p1 = $vals['value'];
        } elseif ($vals['value_type'] == 'P2'){
            $p2 = $vals['value'];
        }
    }
    if ($p1 & $p2) {
        $aqi = calcAqi($p1,$p2);
        if ($aqi < 301){
            $sql .= "INSERT INTO toxsense (lat, lon, aqi, ts, source)
            VALUES ('$lat', '$lon', '$aqi', '$ts', '1');";
        }
    }
}


$servername = $_SERVER['MYSQL_HOST'];
$username = $_SERVER['MYSQL_USER'];
$password = $_SERVER['MYSQL_PASSWORD'];
$db = $_SERVER['MYSQL_DATABASE'];

$conn = new mysqli($servername, $username, $password, $db);
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

if ($conn->query("SHOW TABLES LIKE 'toxsense';")->num_rows == 0) {
    $sql = "CREATE TABLE toxsense (
        id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        lat FLOAT,
        lon FLOAT,
        aqi SMALLINT,
        ts INT,
        source TINYINT
        );";
}

$r1 = $conn->multi_query($sql."DELETE FROM toxsense WHERE (source = '1' and ts != '$ts') OR ('$ts' - ts > 3600);");

if ($r1) {
    echo "New records created successfully\n";
  } else {
    die("Error: " . $conn->error);
}
