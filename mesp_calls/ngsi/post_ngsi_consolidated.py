import requests
import datetime
from time import time
from time import sleep
import sys



notthecorrectdate = "2016-03-15T11:00:00/2016-03-15T12:00:00"


def posttoorion_airquality (UNIQUEID, GPS_x,GPS_y, EPOCH, GAS_1):

    # consider converting epoch to date e.g. now = datetime.datetime(EPOCH)
    now = datetime.datetime.now()

    # check what values can be exported from GAS_1 value e.g.  airQualityIndex, CO value and fill the respective items bellow


    json_airquality = {
        "id": "AirQualityObserved:ntua:"+UNIQUEID,
        "type": "AirQualityObserved",
        "dateObserved": {
            "value": notthecorrectdate,
            "type": "Date"
        },
        "airQualityLevel": {
            "value": "moderate",
            "type": "text"
        },
        "CO": {
            "value": GAS_1,
            "metadata": {
                "unitCode": {
                    "value": "GP"
                }
            }
        },
        "NO": {
            "value": GAS_1,
            "type": "text",
            "metadata": {
                "unitCode": {
                    "value": "GQ"
                }
            }
        },
        "location": {
            "type": "geo:json",
            "value": {
                "type": "Point",
                "coordinates": [GPS_x,GPS_y]
            }
        },
        "airQualityIndex": {
            "value": 65,
            "type": "text"
        }
    }
    url = 'http://localhost:1026/v2/entities?options=keyValues'
    headers = {'Accept': 'application/json'}
    print json_airquality

    json_bytes = sys.getsizeof(json_airquality)
    headers_bytes = sys.getsizeof(headers)
    total = json_bytes + headers_bytes
    print json_bytes, headers_bytes, total

    response = requests.post(url, headers=headers, json=json_airquality)
    print(str(response))
    return response




def posttoorion_flame_alert (UNIQUEID, GPS_x,GPS_y, EPOCH, FLAME_1):
    # consider converting epoch to date e.g. now = datetime.datetime(EPOCH)
    now = datetime.datetime.now()

    json_forest_fire_flame = {
        "id": "Alert:security:forestFireFlame:"+UNIQUEID,
        "type": "Alert",
        "category": {
            "value": "security",
            "type": "text"
        },
        "subCategory": {
            "value": "forestFire",
            "type": "text"
        },
        "severity": {
            "value": FLAME_1,
            "type": "text"
        },
        "location": {
            "value": {
                "type": "Point",
                "coordinates": [GPS_x,GPS_y]
            },
            "type": "geo:json"
        },
        "dateIssued": {
            "value": "2017-01-02T09:25:55.00Z",
            "type": "date"
        },
        "description": {
            "value": "forest fire detected in the area of xxxx",
            "type": "text"
        },
        "alertSource": {
            "value": "Based on iMESP flame detector",
            "type": "text"
        }
    }

    url = 'http://localhost:1026/v2/entities?options=keyValues'
    headers = {'Accept': 'application/json'}
    print json_forest_fire_flame

    json_bytes = sys.getsizeof(json_forest_fire_flame)
    headers_bytes = sys.getsizeof(headers)
    total = json_bytes + headers_bytes
    print json_bytes, headers_bytes, total

    response = requests.post(url, headers=headers, json=json_forest_fire_flame)
    print(str(response))
    return response


def posttoorion_image_alert (UNIQUEID, GPS_x,GPS_y, EPOCH, classification_image):
    # consider converting epoch to date e.g. now = datetime.datetime(EPOCH)
    now = datetime.datetime.now()

    json_forest_fire_image = {
        "id": "Alert:security:forestFireImage:"+UNIQUEID,
        "type": "Alert",
        "category": {
            "value": "security",
            "type": "text"
        },
        "subCategory": {
            "value": "forestFire",
            "type": "text"
        },
        "severity": {
            "value": classification_image,
            "type": "text"
        },
        "location": {
            "value": {
                "type": "Point",
                "coordinates": [GPS_x,GPS_y]
            },
            "type": "geo:json"
        },
        "dateIssued": {
            "value": "2017-01-02T09:25:55.00Z",
            "type": "date"
        },
        "description": {
            "value": "forest fire detected in the area of xxxx",
            "type": "text"
        },
        "alertSource": {
            "value": "Based on iMESP image classification engine",
            "type": "text"
        }
    }

    url = 'http://localhost:1026/v2/entities?options=keyValues'
    headers = {'Accept': 'application/json'}
    print json_forest_fire_image

    json_bytes = sys.getsizeof(json_forest_fire_image)
    headers_bytes = sys.getsizeof(headers)
    total = json_bytes + headers_bytes
    print json_bytes, headers_bytes, total

    response = requests.post(url, headers=headers, json=json_forest_fire_image)
    print(str(response))
    return response



def posttoorion_greenspace (UNIQUEID,GPS_x, GPS_y, EPOCH, HUMIDITY_1, TEMP_AIR_1, TEMP_SOIL_1):

    # consider converting epoch to date e.g. now = datetime.datetime(EPOCH)
    now = datetime.datetime.now()

    json_greenspace = {
            "id": "Greenspace:rafina:1"+UNIQUEID,
            "type": "GreenspaceRecord",

            "location": {
                "value": {
                    "type": "Point",
                    "coordinates": [
                        GPS_x,
                        GPS_y
                    ]
                },
                "type": "geo:json"
            },

            "dateObserved": {
                "value": notthecorrectdate,
                "type": "date"
            },
            "soilTemperature": {
                "value": TEMP_SOIL_1,
                "type": "Number"
            },
            "relativeHumidity": {
                "value": HUMIDITY_1,
                "type": "Number"
            },

            "Temperature": {
                "value": TEMP_AIR_1,
                "type": "Number"
            },
            "refAirQualityObserved": {
                "value": "unique-id-of-airQuality",
                "type": "Reference"
            },
            "refAlert": {
                "value": ["Alert:security:forestFire:123",
                          "Alert:weather:fireRisk:123",
                          ],
                "type": "Reference"
            },
            "refDevice": {
                "value": ["urn:ngsi:Device:RaspberryPi:d9e7-43cd-9c68-1111",
                          "urn:ngsi:Device:Arduino:d9e7-43cd-9c68-1111"],
                "type": "Reference"
            }
    }

    url = 'http://localhost:1026/v2/entities?options=keyValues'
    headers = {'Accept': 'application/json'}
    print json_greenspace

    json_bytes = sys.getsizeof(json_greenspace)
    headers_bytes = sys.getsizeof(headers)
    total = json_bytes + headers_bytes
    print json_bytes, headers_bytes, total

    response = requests.post(url, headers=headers, json=json_greenspace)
    print(str(response))
    return response


UNIQUEID = "kk"
GPS_x = -3.712247222222222
GPS_y = 40.423852777777775

EPOCH = "yy"
HUMIDITY_1 = "cc"
FLAME_1= "ll"
TEMP_AIR_1 = "hh"
GAS_1 = "pp"
TEMP_SOIL_1 = "oo"
IMAGE = ""


# UNIQUEID;NODEID;GPS#1;EPOCH;HUMIDITY#1;FLAME#1;TEMP-AIR#1;GAS#1;TEMP-SOIL#1;
# GAS#1 will be modeled as airquality through the function posttoorion_airquality
# FLAME#1  will be modeled as alert through the function  posttoorion_flam
#  HUMIDITY_1, TEMP_AIR_1, TEMP_SOIL_1  will be modeled as greenspace through the function posttoorion_greenspace

print "posting GAS_1"
posttoorion_airquality (UNIQUEID, GPS_x,GPS_y, EPOCH,GAS_1)
print "posting GAS_1:done"

print "posting FLAME#1"
posttoorion_flame_alert (UNIQUEID,GPS_x, GPS_y, EPOCH, FLAME_1)
print "posting flame:done"

print "posting IMAGE"
posttoorion_image_alert (UNIQUEID,GPS_x, GPS_y, EPOCH, IMAGE)
print "posting IMAGE:done"

print "posting greenspace"
posttoorion_greenspace (UNIQUEID,GPS_x, GPS_y, EPOCH, HUMIDITY_1, TEMP_AIR_1, TEMP_SOIL_1)
print "posting greenspace:done"