import requests
import datetime
from time import time
from time import sleep
import sys

#  converting epoch to date e.g. now = datetime.datetime(EPOCH) or sth
# I use temporary the notthecorrectdate variable
notthecorrectdate = "2016-03-15T11:00:00/2016-03-15T12:00:00"


def posttoorion_airquality (UNIQUEID, GPS_x,GPS_y, EPOCH, GAS_1):

    # check what values can be exported from GAS_1 value e.g.  airQualityIndex, CO value and fill the respective items bellow

    json_airquality = {"@context": [
        "https://forge.etsi.org/gitlab/NGSI-LD/NGSI-LD/raw/master/coreContext/ngsi-ld-core-context.json",
        "https://raw.githubusercontent.com/GSMADeveloper/NGSI-LD-Entities/master/examples/Air-Quality-Observed-context.jsonld"
    ],
        "id": "urn:ngsi-ld:AirQualityObserved:"+UNIQUEID,
        "type": "AirQualityObserved",
        "entityVersion": 2.0,
        "name": {
            "type": "Property",
            "value": "MESP"
        },
        "location": {
            "type": "GeoProperty",
            "value": {
                "type": "Point",
                "coordinates": [GPS_x,GPS_y]
            }
        },
        "observedAt": {
            "type": "Property",
            "value": notthecorrectdate
        },
        "airQualityIndex": {
            "type": "Property",
            "value": {
                "value": 65,
                "unitText": "US EPA AQI"
            },
            "observedAt": "2017-05-04T12:30:00Z"
        },
        "CO": {
            "type": "Property",
            "value": {
                "value": GAS_1,
                "unitText": "microgramme per cubic metre"
            },
            "unitCode": "GQ",
            "observedAt": notthecorrectdate
        },
        "NO": {
            "type": "Property",
            "value": {
                "value": GAS_1,
                "unitText": "microgramme per cubic metre"
            },
            "unitCode": "GQ",
            "observedAt": notthecorrectdate
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




def posttoorion_flame (UNIQUEID, GPS_x,GPS_y, EPOCH, FLAME_1):
    # consider converting epoch to date e.g. now = datetime.datetime(EPOCH)
    now = datetime.datetime.now()


    json_forest_fire ={"@context": [
        "https://forge.etsi.org/gitlab/NGSI-LD/NGSI-LD/raw/master/coreContext/ngsi-ld-core-context.json",
        "https://raw.githubusercontent.com/nikoskal/mesp/mdpi/etsi_ngsild_datamodels/specs/Alert/schema.json"
        ],
        "id": "urn:ngsi-ld:Alert:security:"+UNIQUEID,
        "type": "Alert",
        "source": "GSMA",
        "dataProvider": "GSMA",
        "entityVersion": 2.0,

        "category": {
            "type": "Property",
            "value": "security"
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
            "value": "Based on iMESP image classification engine",
            "type": "text"
        }
    }



    url = 'http://localhost:1026/v2/entities?options=keyValues'
    headers = {'Accept': 'application/json'}
    print json_forest_fire

    json_bytes = sys.getsizeof(json_forest_fire)
    headers_bytes = sys.getsizeof(headers)
    total = json_bytes + headers_bytes
    print json_bytes, headers_bytes, total

    response = requests.post(url, headers=headers, json=json_forest_fire)
    print(str(response))
    return response




def posttoorion_greenspace (UNIQUEID,GPS_x, GPS_y, EPOCH, HUMIDITY_1, TEMP_AIR_1, TEMP_SOIL_1):

    # consider converting epoch to date e.g. now = datetime.datetime(EPOCH)
    now = datetime.datetime.now()

    json_forest_fire = {"@context": [
        "https://forge.etsi.org/gitlab/NGSI-LD/NGSI-LD/raw/master/coreContext/ngsi-ld-core-context.json",
        "https://raw.githubusercontent.com/GSMADeveloper/NGSI-LD-Entities/master/examples/Agri-Parcel-Record-context.jsonld"
        ],

            "id": "urn:ngsi-ld:AgriParcelRecord:"+UNIQUEID,
            "type": "Agri-Parcel",

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
                "type": "Property",
                "value": TEMP_SOIL_1,
                "unitCode": "CEL",
                "observedAt": notthecorrectdate
            },
            "relativeHumidity": {
                "type": "Property",
                "value": HUMIDITY_1,
                "unitCode": "CEL",
                "observedAt": notthecorrectdate
            },

            "Temperature": {
                "type": "Property",
                "value": TEMP_AIR_1,
                "unitCode": "CEL",
                "observedAt": notthecorrectdate
            },
            "refAirQualityObserved": {
                "value": "unique-id-of-airQuality",
                "type": "Reference"
            },
            "refAlert": {
                "value": ["Alert:security:forestFire:123",
                          "Alert:weather:fireRisk:123"],
                "type": "Reference"
            },
            "refDevice": {
                "value": ["urn:ngsi:Device:RaspberryPi:d9e7-43cd-9c68-1111",
                          "urn:ngsi:Device:Arduino:d9e7-43cd-9c68-1111"],
                "type": "Reference"
            }
    }


UNIQUEID = "kk"
GPS_x = -3.712247222222222
GPS_y = 40.423852777777775

EPOCH = "yy"
HUMIDITY_1 = "cc"
FLAME_1= "ll"
TEMP_AIR_1 = "hh"
GAS_1 = "pp"
TEMP_SOIL_1 = "oo"


# UNIQUEID;NODEID;GPS#1;EPOCH;HUMIDITY#1;FLAME#1;TEMP-AIR#1;GAS#1;TEMP-SOIL#1;
# GAS#1 will be modeled as airquality through the function posttoorion_airquality
# FLAME#1  will be modeled as alert through the function  posttoorion_flam
#  HUMIDITY_1, TEMP_AIR_1, TEMP_SOIL_1  will be modeled as greenspace through the function posttoorion_greenspace

print "posting GAS_1"
posttoorion_airquality (UNIQUEID, GPS_x,GPS_y, EPOCH,GAS_1)
print "posting GAS_1:done"

print "posting FLAME#1"
posttoorion_flame (UNIQUEID,GPS_x, GPS_y, EPOCH, FLAME_1)
print "posting flame:done"

print "posting greenspace"
posttoorion_greenspace (UNIQUEID,GPS_x, GPS_y, EPOCH, HUMIDITY_1, TEMP_AIR_1, TEMP_SOIL_1)
print "posting greenspace:done"