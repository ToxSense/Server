from typing import Optional

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

import concurrent.futures, os, math, time

from starlette.requests import Request
from getWind import getWind
from osmDL import genMaps

import pymysql as con

import numpy as np
import pandas as pd

from tensorflow.keras.models import load_model

cwd = os.path.dirname(os.path.realpath(__file__))

class data(BaseModel):
    lat: float
    lon: float
    aqi: Optional[int] = None
    img: Optional[str] = None

def createImg(binImgs):
    imgs = list()
    for value in binImgs:
        img = np.zeros((64, 64, 1), dtype=np.uint8)
        j=0
        for x in range(64):
            for y in range(64):
                img[x,y] = int(value[j])
                j += 1
        imgs.append(img)
    return np.array(imgs, dtype=np.uint8)

def cMinMax(df):
    df[['aqi1', 'aqi2', 'aqi3']] = df[['aqi1', 'aqi2', 'aqi3']] / 300.00
    df[['aqi1dir', 'aqi2dir', 'aqi3dir', 'winddir']] = df[['aqi1dir', 'aqi2dir', 'aqi3dir', 'winddir']] / 360.00
    df['windspeed'] = df['windspeed'] / 220
    return df

def getAqiDir(lat1, lon1, lat2, lon2):

    ##get distance --->>> TO REVIEW!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    x = lat1 - lat2
    y = lon1 - lon2

    earthRadius=6378137

    xMeters = (x / (180/math.pi)) * earthRadius
    yMeters = (y / (180/math.pi)) * (earthRadius*math.cos(math.pi*x/180))

    aqiDist = int(math.sqrt(xMeters**2 + yMeters**2))

    ##get direction in °
    aqiDir = int(360 * (math.acos(xMeters/(1+aqiDist)))/math.pi)
    if yMeters < 0:
        aqiDir = 360 - aqiDir


    return aqiDir

def latLonAI(latLons):
    aqis = []
    error = []
    info = []
    data = pd.DataFrame(columns=['aqi1','aqi1dir','aqi2','aqi2dir','aqi3','aqi3dir','windspeed','winddir'], dtype=np.int16)
    maps = genMaps()
    curErr = False
    dbErr = False
    

    for lat, lon in latLons:
        maps.add(lat, lon)
    maps.generate()
    mapsec = createImg(maps.maps.values())


    for latLon in latLons:
        
        lat = latLon[0]
        lon = latLon[1]
        try:
            db = con.connect(
                host=os.environ['MYSQL_HOST'],
                user=os.environ['MYSQL_USER'],
                password=os.environ['MYSQL_PASSWORD'],
                database=os.environ['MYSQL_DATABASE']
                )
            cur = db.cursor()
        except:
            error.append("DB-Connection failed")
            dbErr = True


        if dbErr == False:
        #get 3 closest aqi

            cur.execute(" \
                SELECT aqi, lat, lon, POW(69.1 * (lat - %s), 2) + POW(69.1 * (%s - lon) * COS(lat / 57.3), 2) AS distance \
                FROM toxsense \
                HAVING distance < 25 AND lat != %s AND lon != %s \
                ORDER BY distance \
                LIMIT 3 \
                ", (lat, lon, lat, lon))

            threeAqis = cur.fetchall()
            db.close()

            try:
                aqi1 = threeAqis[0][0]
                aqi1dir = getAqiDir(threeAqis[0][1], threeAqis[0][2], lat, lon)
                aqi2 = threeAqis[1][0]
                aqi2dir = getAqiDir(threeAqis[1][1], threeAqis[1][2], lat, lon)
                aqi3 = threeAqis[2][0]
                aqi3dir = getAqiDir(threeAqis[2][1], threeAqis[2][2], lat, lon)
            except:
                error.append('not enough data!')
                curErr == True
                break

            #get wdir & wspd
        if curErr == False:
            winddf = getWind(lat, lon)
            if winddf is None:
                curErr = True
                info.append('No winddata found, interpolating')
                wspd = 0
                wdir = 0
            else:
                try:
                    wspd = int(winddf.wspd[0])
                    wdir = int(winddf.wdir[0])
                except:
                    try:
                        wspd = int(winddf.wspd[1])
                        wdir = int(winddf.wdir[1])
                    except:
                        curErr = True
                        info.append('No winddata found, interpolating')
                        wspd = 0
                        wdir = 0

        data = data.append({'aqi1':aqi1,'aqi1dir': aqi1dir,'aqi2': aqi2,'aqi2dir': aqi2dir,'aqi3': aqi3,'aqi3dir': aqi3dir,'windspeed': wspd,'winddir': wdir}, ignore_index=True)



                    


 
    #TF calcs

    intData = data.copy()
    if curErr == False: 
        cMinMax(data)
        try:

            model = load_model(cwd + "/model")
            aqis = model.predict([data, mapsec])

            """ if aqi < 0:
                aqi=0 """

        except Exception as e:
            curErr = True
            info.append(f"TF Error: ({e}), interpolating")



    if curErr == True:
        for row in intData.iterrows()[1]:
            aqis.append(int((row['aqi1'] + row['aqi2'] + row['aqi3']) / 3))


    return aqis, info, error



app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = [
    "https://toxsense.de",
    "http://toxsense.de",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
@limiter.exempt
def read_root():
    return r"For api description please consult the <a href='/docs'>docs</a>"


@app.post("/")
@limiter.limit("30/minute")
async def process_data(data: data, request: Request):
    selfaqi = None
    aqiN = None
    aqiE = None
    aqiS = None
    aqiW = None
    error = []
    info = None
    ts = time.time()

    #init list to calc
    latLons = []
    latLons.append((data.lat, data.lon))
    if data.aqi:
        latLons.append((data.lat + 0.001, data.lon)) #N
        latLons.append((data.lat, data.lon + 0.001)) #E
        latLons.append((data.lat - 0.001, data.lon)) #S
        latLons.append((data.lat, data.lon - 0.001)) #W

    allaqis = latLonAI(latLons)

    #save selfaqi
    try:     
        selfaqi = int(allaqis[0][0])
    except Exception as e:
        error.append(e)
    info = allaqis[1]

    #get errors
    if allaqis[2]:
        error.append(allaqis[2])

    if error:
        return {"error":error}
    elif data.aqi:
        #calc selfaqi avg from headband and server ai
        selfaqi = (selfaqi + data.aqi) / 2

        #save calc data to mysqldb
        db = con.connect(
            host=os.environ['MYSQL_HOST'],
            user=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PASSWORD'],
            database=os.environ['MYSQL_DATABASE']
        )
        cur = db.cursor()

        if data.img:
            imgf = open(cwd + f"/imgdb/{selfaqi}_{time.time_ns()}.jpg", 'wb')
            imgbytes = bytes(data.img, 'utf-8')
            imgf.write(imgbytes)
            imgf.close()
        
        cur.execute("INSERT INTO toxsense (lat, lon, aqi, ts, source) VALUES ('%s', '%s', '%s', '%s', '0')", (data.lat, data.lon, int(selfaqi), ts))
        """ for i in range(1,len(allaqis)):
            cur.execute("INSERT INTO toxsense (lat, lon, aqi, ts, source) VALUES ('%s', '%s', '%s', '%s', '0')", (latLons[i][0], latLons[i][1], allaqis[i][0], ts)) """
        db.commit()
        db.close()

        #possible usage for absolute aqis
        aqiN = allaqis[0][1]
        aqiE = allaqis[0][2]
        aqiS = allaqis[0][3]
        aqiW = allaqis[0][4]
        return {"selfaqi":int(selfaqi), "aqiN": int(aqiN), "aqiE": int(aqiE), "aqiS": int(aqiS), "aqiW": int(aqiW), "info": info}

        #usage for relative aqis (for the headband)
        """ minaqi = min([allaqis[1][0],allaqis[2][0], allaqis[3][0], allaqis[4][0]])
        relmaxaqi = max([allaqis[1][0],allaqis[2][0], allaqis[3][0], allaqis[4][0]]) - minaqi
        if relmaxaqi != 0:
            aqiN = (allaqis[1][0] - minaqi) / relmaxaqi
            aqiE = (allaqis[2][0] - minaqi) / relmaxaqi
            aqiS = (allaqis[3][0] - minaqi) / relmaxaqi
            aqiW = (allaqis[4][0] - minaqi) / relmaxaqi
        else:
            aqiN = 0
            aqiE = 0
            aqiS = 0
            aqiW = 0

        #return to headband
        return {"perN": aqiN, "perE": aqiE, "perS": aqiS, "perW": aqiW, "info": info} """
    else:
        source = 2
        #save calc data to mysqldb
        db = con.connect(
            host=os.environ['MYSQL_HOST'],
            user=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PASSWORD'],
            database=os.environ['MYSQL_DATABASE']
        )
        cur = db.cursor()
        if info == "TF Error, interpolating" or info == 'No winddata found, interpolating':
            source = 3
        cur.execute("INSERT INTO toxsense (lat, lon, aqi, ts, source) VALUES ('%s', '%s', '%s', '%s', '%s')", (data.lat, data.lon, selfaqi, ts, source))
        db.commit()
        db.close()

        #return to map
        return {"selfaqi":selfaqi, "info":info, "source":source}
 