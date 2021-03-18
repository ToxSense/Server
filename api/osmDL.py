#!/usr/bin/python

from PIL import Image
import os
import subprocess

cwd = os.path.dirname(os.path.realpath(__file__))

class genMaps:
    def __init__(self):
        self.coordinatesList = []
        self.maperiExecPath = f"{cwd}/Maperitive/Maperitive.Console.exe"
        self.maps = {}
    
    def add(self, lat, lon):
        self.coordinatesList.append((lat,lon))

    def generate(self,io=True):
        dlScript = open(cwd + '/Maperitive/scripts/dlscript.mscript', 'w')
        i = 0
        latA = self.coordinatesList[0][0] - 0.003
        latB = self.coordinatesList[0][0] + 0.003
        lonA = self.coordinatesList[0][1] - 0.003
        lonB = self.coordinatesList[0][1] + 0.003

        dlScript.write(f'set-geo-bounds {lonA},{latA},{lonB},{latB}\ndownload-osm-overpass bounds={lonA},{latA},{lonB},{latB} service-url="https://overpass.kumi.systems/api/" ' + r'query="way[building]($b$);out;>;out qt;"' + '\n')
            
        for co in self.coordinatesList:
            latA = co[0] - 0.001
            latB = co[0] + 0.001
            lonA = co[1] - 0.001
            lonB = co[1] + 0.001

            dlScript.write(f'set-geo-bounds {lonA},{latA},{lonB},{latB}\nexport-bitmap file=temp{i}.png width=64 height=64 zoom=16\n')
            i += 1
        dlScript.write('exit\n')
        dlScript.close()

        constrCmd = ["mono",self.maperiExecPath, cwd + '/Maperitive/scripts/basicsetting.mscript', cwd + '/Maperitive/scripts/dlscript.mscript']
        subprocess.run(constrCmd, cwd=cwd+'/Maperitive/scripts/', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
        i = 0
        for co in self.coordinatesList:
            image = Image.open(cwd + f'/Maperitive/scripts/temp{i}.png').convert("L")

            if io == True:
                binarystring = ""

                for x in range(image.width):
                    for y in range(image.height):
                        binarystring += str(round(image.getpixel((x,y)) / 255))

                self.maps.update({(co[0],co[1]):binarystring})
            elif io == False:
                self.maps.update({(co[0],co[1]):image})

            #os.remove(cwd + f'/Maperitive/scripts/temp{i}.png')
            #os.remove(cwd + f'/Maperitive/scripts/temp{i}.png.georef')
            i += 1