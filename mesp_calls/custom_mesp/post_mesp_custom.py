import requests
import datetime
from time import time
from time import sleep
import sys


def posttoorion(UNIQUEID, GPS_1, EPOCH, HUMIDITY_1, FLAME_1,TEMP_AIR_1,GAS_1,TEMP_SOIL_1  ):
    print("parse snapshot")
    print UNIQUEID, GPS_1, EPOCH, HUMIDITY_1, FLAME_1, TEMP_AIR_1, GAS_1, TEMP_SOIL_1

    pts = datetime.datetime.now().strftime('%s')

    url = 'http://localhost:1026/v2/entities?options=keyValues'
    headers = {'Accept': 'application/json'}



    json_mesp_measurment = {
        "id": UNIQUEID,
        "type": "MespMeasurment",
        "dateObserved": {
            "value": EPOCH
        },
        "GPS_1": {
            "value": GPS_1
        },
        "HUMIDITY_1": {
            "value": HUMIDITY_1
        },
        "FLAME_1": {
            "value": FLAME_1,
        },
        "TEMP_AIR_1": {
            "value": TEMP_AIR_1
        },
        "GAS_1": {
            "value": TEMP_AIR_1
        },
        "TEMP_SOIL_1": {
            "value": TEMP_AIR_1
        }
}



    print json_mesp_measurment

    json_bytes = sys.getsizeof(json_mesp_measurment)
    headers_bytes = sys.getsizeof(headers)
    total = json_bytes + headers_bytes
    print json_bytes,headers_bytes, total

    response = requests.post(url, headers=headers, json=json_mesp_measurment)
    print(str(response))
    return response

UNIQUEID = "kk"
GPS_1 = "xx"
EPOCH = "yy"
HUMIDITY_1 = "cc"
FLAME_1= "ll"
TEMP_AIR_1 = "hh"
GAS_1 = "pp"
TEMP_SOIL_1 = "oo"


# UNIQUEID;NODEID;GPS#1;EPOCH;HUMIDITY#1;FLAME#1;TEMP-AIR#1;GAS#1;TEMP-SOIL#1;
posttoorion(UNIQUEID, GPS_1, EPOCH, HUMIDITY_1, FLAME_1,TEMP_AIR_1,GAS_1,TEMP_SOIL_1  )
