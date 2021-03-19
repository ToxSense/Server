# Learning Atmospheres - ToxSense 

## Online Server

The calculated air quality index is sent to the server, together with the users gps location and the captured image. This “POST-Request” contains a JSON-String-Dictionary with all the data. The request is captured by an FastAPI-Server [FastAPI], a server handling the request in Python-programming-language [Python] at https://api.ToxSense.de. The JSON-String is decoded into a Python dictionary for further processing.

The process described in the next part is not only applied to the actual latitude and longitude of the user, but also for surrounding positions approximately 10 meters apart. The first step consists of the generation of an urban figure ground plan, using the Maperitive [Maperitive] utility, for the user’s exact position with an approximate radius of 100 meters, as this represents an elemental input for the AI. Then, from the existing ToxSense database, the closest three sensor values together with their direction relative to the users position are imported into the inference dataset. The last data collected is composed out of the current wind speed in meters per second and the wind direction, collected using the Meteostat library. [ Meteostat] Finally, using the gathered data, an inference on the trained TensorFlow-Model [TensorFlow] is run. As a result a single AQI-value is returned to the main function.

Now the image sent by the users headband and the calculated AQI is saved into an independent database, later used for retraining and updating the AI-model on the headband, ensuring more accurate results only through a widespread usage of the headband. Now the server returns a new JSON-array containing the calculated aqi, on one hand for the users position, on the other hand for positions in every direction from the user, making it possible to make a walking suggestion, together with some informational data displayed later on the smartphone application. Lastly the data is saved into the main ToxSense-database, making it available online on the ToxSense Map viewable by everyone.

This Website (https://ToxSense.de) is programmed in HTML5, PHP8, CSS3, but the main functions are deployed with JavaScript. The main frame shows a Leaflet-Map [Leaflet, OpenStreetMap], combined with its Heatmap-Plugin [Heatmap.js]. The third layer is only shown on a high zoom-level, displaying clickable circles that open pop-ups revealing the absolute AQI-values. When the map is loaded in the browser, the JavaScript makes an AJAX-request to an PHP-script, that returns all the values in the ToxSense-database. This Database is running on an MariaDB [MariaDB] server queryable with MySQL and contains all AQI-data from the ToxSense-Project, but it is also synchronized with the sensor.community [Sensor.community] database for very accurate base values. 

The AQIs are then displayed as a modified heatmap, that, instead of adding the values of closest points together, always calculates and displays the averaged figure. All the different server applications are deployed in virtual environments, ensuring an easy reproduction and deployment on any platform.

## Credits

This project is imagined and created by Timo Bilhöfer, Markus Pfaff and Maria Rădulescu.

As part of the seminar *Learning Atmospheres* in the winter-semester 2020/21 it is supported by Irina Auernhammer, Silas Kalmbach and Prof. Lucio Blandini from the[ Institute for Lightweight Structures and Conceptual Design (**ILEK**)](https://www.ilek.uni-stuttgart.de/) and is also part of the[ Collaborative Research Centre 1244 (**SFB 1244**)](https://www.sfb1244.uni-stuttgart.de/).



## **Bibliography**

Air Protection and **Climate Policy Office**, Department of Air Quality and Education Monitoring in **Warsaw** (**2020**), Warsaw’s holistic approach to reduce air pollution, https://breathelife2030.org/news/warsaws-holistic-approach-reduce-air-pollution/ Accessed 2021/03/16



**Badach**, Joanna; Voordeckers, Dimitri; Nyka, Lucyna; van Acker, Maarten (**2020**): A framework for Air Quality Management Zones - Useful GIS-based tool for urban planning: Case studies in Antwerp and Gdańsk. In Building and Environment 174, p. 106743. DOI: 10.1016/j.buildenv.2020.106743.



**BreathLife** (**2016**): https://breathelife2030.org/solutions/citywide-solutions/ Accessed 2021/03/16



**Climate & Clean Air Coalition** (**2020**): World Cities day event focuses on how health, climate and urban air pollution are interlinked, https://breathelife2030.org/news/world-cities-day-event-focuses-health-climate-urban-air-pollution-interlinked/ Accessed 2021/03/16



**Das**, Ritwajit (**2020**) How community-based air quality monitoring is helping the city of Bengaluru fight back against air pollution, https://breathelife2030.org/news/community-based-air-quality-monitoring-helping-city-bengaluru-fight-back-air-pollution/ Accessed 2021/03/16

**Goodfellow**, Ian; Bengio, Yoshua; Courville Aaron. (**2016**): *Deep Learning*. MIT Press.

**Institute of hygiene and environment, Hamburg**. Leuchtbakterientest. Accessed 2021/03/17. https://www.hamburg.de/hu/biotestverfahren/2604448/leuchtbakterientest/

**Kang**, Gaganjot Kaur; Gao, Jerry Zeyu; Chiao, Sen; Lu, Shengqiang; Xie, Gang (**2018**): Air Quality Prediction: Big Data and Machine Learning Approaches. In IJESD 9 (1), pp. 8–16. DOI: 10.18178/ijesd.2018.9.1.1066.

**Larson**, Jeff; Mattu, Surya; Kirchner, Lauren; Angwin, Julia (**2016**): How We Analyzed the COMPAS Recidivism Algorithm

**Liao**, Xiong; Tu, Hong; Maddock, Jay E.; Fan, Si; Lan, Guilin; Wu, Yanyan et al. (**2015**): Residents’ perception of air quality, pollution sources, and air pollution control in Nanchang, China. In Atmospheric Pollution Research 6 (5), pp. 835–841. DOI: 10.5094/APR.2015.092.

**Nikolopoulou**, Marialena. (**2009**). PERCEPTION OF AIR POLLUTION AND COMFORT IN THE URBAN, Conference: CISBAT International Scientific Conference, Lausanne

**Nisky**, Ilana; Hartcher-O’Brien, Jess; Wiertlewski, Michaël; Smeets, Jeroen (**2020**): Haptics: Science, Technology, Applications. Cham: Springer International Publishing (12272).

**Peng**, Minggang; Zhang, Hui; Evans, Richard D.; Zhong, Xiaohui; Yang, Kun (**2019**): Actual Air Pollution, Environmental Transparency, and the Perception of Air Pollution in China. In *The Journal of Environment & Development* 28 (1), pp. 78–105. DOI: 10.1177/1070496518821713.

**Rosenblatt**, Frank (**1958**): The perceptron - a probabilistic model for information storage and organization in the brain.

**Smedley**, Tim. **2019**/11/15. The toxic killers in our air too small to see. Accessed 2021/03/14. https://www.bbc.com/future/article/20191113-the-toxic-killers-in-our-air-too-small-to-see

**Sokhanvar**, Saeed S. (**2013**): Tactile sensing and displays. Haptic feedback for minimally invasive surgery and robotics. Chichester, West Sussex, U.K.: John Wiley & Sons.

**Spiroska**, Jana; Rahman, Asif; Pal, Saptarshi (**2011**): Air Pollution in Kolkata: An Analysis of Current Status and Interrelation between Different Factors. In South East European University Review 8 (1). DOI: 10.2478/v10306-012-0012-7.

**Valueva**, M.V.; Nagornov N.N.; Lyakhov, P.A.; Valuev, G.V.; Chervyakov, N.I. (**2020**) Application of the residue number system to reduce hardware costs of the convolutional neural network implementation, Mathematics and Computers in Simulation. https://doi.org/10.1016/j.matcom.2020.04.031.

**VISATON**. **2010**/04. Basic principles of exciter-technology. Accessed 2021/03/14. 

**Vu**, Tuan V.; Shi, Zongbo; Cheng, Jing; Zhang, Qiang; He, Kebin; Wang, Shuxiao; Harrison, Roy M. (**2019**): Assessing the impact of clean air action on air quality trends in Beijing using a machine learning technique. In Atmos. Chem. Phys. 19 (17), pp. 11303–11314. DOI: 10.5194/acp-19-11303-2019.

**World Health Organization (2006)**: Air quality guidelines. Global update 2005 : particulate matter, ozone, nitrogen dioxide, and sulfur dioxide. Copenhagen: World Health Organization.

**Whitney**, Matt; Quin, Hu (**2021**): How China is tackling air pollution with big data, https://breathelife2030.org/news/china-tackling-air-pollution-big-data/ Accessed 2021/03/16

**Wu**, Yi-Chen; Shiledar, Ashutosh; Li, Yi-Cheng; Wong, Jeffrey; Feng, Steve; Chen, Xuan et al. (**2017**): Air quality monitoring using mobile microscopy and machine learning. In Light, science & applications 6 (9), e17046. DOI: 10.1038/lsa.2017.46.



## **Programming resources:**

**1** **Android Bluetooth**. Majdi_la. (Sample Code) https://stackoverflow.com/questions/13450406/how-to-receive-serial-data-using-android-bluetooth. CC BY-SA 3.0.

**2** **Android GPS**. Azhar. (Sample Code) https://www.tutorialspoint.com/how-to-get-the-current-gps-location-programmatically-on-android-using-kotlin. Terms apply.

**3** **Android TFlite**. Anupamchugh. (Sample Code) anupamchugh/AndroidTfLiteCameraX. Pending request.

**4** **FastAPI**. Sebastián Ramírez. (Library) tiangolo/fastapi. https://fastapi.tiangolo.com/. MIT-License.

**5** **I2cdevlib**. Jeff Rowberg. (Library) jrowberg/i2cdevlib. MIT-License.

**6** **Keras: Multiple Inputs and Mixed Data**. Adrian Rosebrock. (Sample Code) https://www.pyimagesearch.com/2019/02/04/keras-multiple-inputs-and-mixed-data/

**7** **Leaflet**. Vladimir Agafonkin. (Library) Leaflet/Leaflet. https://leafletjs.com/. BSD-2-Clause.

**8** **Maperitive**. Igor Brejc. (Program) https://maperitive.net. Terms apply.

**9** **Meteostat**. Christian Lamprecht. (DB/Library) https://meteostat.net. CC-BY-NC 4.0/MIT-License.

**10** **officialAQIus**. OpenData Stuttgart. Rewritten by Timo Bilhöfer in Python. (Library) https://github.com/opendata-stuttgart/feinstaub-map-v2/blob/master/src/js/feinstaub-api.js. MIT-License.

**11** **OpenStreetMap**. OpenStreetMap contributors. (DB) https://www.openstreetmap.org/copyright. Terms apply.

**12** **Overpass-API**. Wiktorn. (Docker-Image) wiktorn/Overpass-API. AGPL 3.0.

**13** **Pandas**. Pandas contributors. (Library) https://pandas.pydata.org. BSD-3 Clause

**14** **Python**. Python Software Foundation. (Interpreter) https://python.org. PSF-License

**15** **sensor.community**. (DB) https://archive.sensor.community/. Open Data Commons: Database Contents License (DbCL) v1.0.

**16** **Sqlite3**. (Library & DB Language) https://www.sqlite.org. Public Domain.

**17** **TensorFlow**. TensorFlow Community. (Library & Sample Code) https://www.tensorflow.org. Apache-License 2.0.

**18** **VisionAir**. Harshita Diddee, Divyanshu Sharma, Shivam Grover, Shivani Jindal. (DB) https://vision-air.github.io. MIT-License