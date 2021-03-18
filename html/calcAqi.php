<?php

function calculate_aqi_us($Ih, $Il, $Ch, $Cl, $C) {
    return intval(((($Ih - $Il) / ($Ch - $Cl)) * ($C - $Cl)) + $Il);
}

function aqius($val, $type){
    $index = 0;
    if ($val >= 0){
        if ($type == 'PM10') {
            if (intval($val) <= 54) {
                $index = calculate_aqi_us(50, 0, 54, 0, intval($val));
            } elseif (intval($val) <= 154) {
                $index = calculate_aqi_us(100, 51, 154, 55, intval($val));
            } elseif (intval($val) <= 254) {
                $index = calculate_aqi_us(150, 101, 254, 155, intval($val));
            } elseif (intval($val) <= 354) {
                $index = calculate_aqi_us(200, 151, 354, 255, intval($val));
            } elseif (intval($val) <= 424) {
                $index = calculate_aqi_us(300, 201, 424, 355, intval($val));
            } elseif (intval($val) <= 504) {
                $index = calculate_aqi_us(400, 301, 504, 425, intval($val));
            } elseif (intval($val) <= 604) {
                $index = calculate_aqi_us(500, 401, 604, 505, intval($val));
            } else {
                $index = 500;
            }
        }
        if ($type == 'PM25') {
            if (round($val, 1) <= 12){
                $index = calculate_aqi_us(50, 0, 12, 0, round($val, 1));
            } elseif (round($val, 1) <= 35.4) {
                $index = calculate_aqi_us(100, 51, 35.4, 12.1, round($val, 1));
            } elseif (round($val, 1) <= 55.4) {
                $index = calculate_aqi_us(150, 101, 55.4, 35.5, round($val, 1));
            } elseif (round($val, 1) <= 150.4) {
                $index = calculate_aqi_us(200, 151, 150.4, 55.5, round($val, 1));
            } elseif (round($val, 1) <= 250.4) {
                $index = calculate_aqi_us(300, 201, 250.4, 150.5, round($val, 1));
            } elseif (round($val, 1) <= 350.4) {
                $index = calculate_aqi_us(400, 301, 350.4, 250.5, round($val, 1));
            } elseif (round($val, 1) <= 500.4) {
                $index = calculate_aqi_us(500, 401, 500.4, 350.5, round($val, 1));
            } else {
                $index = 500;
            }
        }
    }
    return $index;
}

function calcAqi($iP1,$iP2){
    $p1 = aqius($iP1, 'PM10');
    $p2 = aqius($iP2, 'PM25');
    if ($p1 >= $p2) {
        return $p1;
    } else {
        return $p2;
    }
}