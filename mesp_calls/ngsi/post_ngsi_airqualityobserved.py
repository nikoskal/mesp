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
    # TODO put here the main values collected by Arduiono sensors
    json_airquality = {
        "id": "AirQualityObserved:ntua:epoch12345",
        "type": "AirQualityObserved",
        "dateObserved": {
            "value": "2016-03-15T11:00:00/2016-03-15T12:00:00"
        },
        "airQualityLevel": {
            "value": "moderate"
        },
        "CO": {
            "value": 500,
            "metadata": {
                "unitCode": {
                    "value": "GP"
                }
            }
        },
        "NO": {
            "value": 45,
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
                "coordinates": [-3.712247222222222, 40.423852777777775]
            }
        },
        "airQualityIndex": {
            "value": 65
        },
        "reliability": {
            "value": 0.7
    }
}



    print json_airquality

    json_bytes = sys.getsizeof(json_airquality)
    headers_bytes = sys.getsizeof(headers)
    total = json_bytes + headers_bytes
    print json_bytes,headers_bytes, total

    response = requests.post(url, headers=headers, json=json_airquality)
    print(str(response))
    return response

dm_attr1 = "kk"
dm_attr2 = "xx"
dm_attr3 = "yy"

posttoorion(dm_attr1, dm_attr2, dm_attr3)

