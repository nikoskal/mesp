import requests
import datetime
from time import time
from time import sleep
import sys


def posttoorion(dm_attr1, dm_attr2, dm_attr3):
    print("parse snapshot")
    print dm_attr1, dm_attr2, dm_attr3

    pts = datetime.datetime.now().strftime('%s')

    url = 'http://localhost:1026/v2/entities?options=keyValues'
    headers = {'Accept': 'application/json'}

    #ngsi format based on:
    # fiware_ngsi_datamodels/specs/Device/DeviceModel/schema.json
    # https://fiware.github.io/dataModels/specs/Device/DeviceModel/schema.json

    json_forest_fire = {
            "id": "Greenspace:rafina:1",
            "type": "GreenspaceRecord",

            "location": {
                "value": {
                    "type": "Point",
                    "coordinates": [
                        -104.99404,
                        39.75621
                    ]
                },
                "type": "geo:json"
            },

            "dateObserved": {
                "value": "2017-01-02T09:25:55.00Z",
                "type": "date"
            },
            "soilTemperature": {
                "value": "12",
                "type": "Number"
            },
            "relativeHumidity": {
                "value": "12",
                "type": "Number"
            },

            "Temperature": {
                "value": "12",
                "type": "Number"
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
                "value": "device:uniqueid:1234",
                "type": "Reference"
            }
    }



    print json_forest_fire

    json_bytes = sys.getsizeof(json_forest_fire)
    headers_bytes = sys.getsizeof(headers)
    total = json_bytes + headers_bytes
    print json_bytes,headers_bytes, total

    response = requests.post(url, headers=headers, json=json_forest_fire)
    print(str(response))
    return response

dm_attr1 = "kk"
dm_attr2 = "xx"
dm_attr3 = "yy"

posttoorion(dm_attr1, dm_attr2, dm_attr3)

