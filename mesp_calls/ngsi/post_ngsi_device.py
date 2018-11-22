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
    # fiware_ngsi_datamodels/specs/Device/Device/schema.json
    # https://fiware.github.io/dataModels/specs/Device/Device/schema.json

    json = {
        "id": "urn:ngsi:Device:RaspberryPi:d9e7-43cd-9c68-1111",
          "type": "Device",
          "source": {
            "value": "http://www.example.com",
            "type": "URL"
          },
          "dataProvider": {
            "value": "OperatorA",
            "type": "Text"
          },
          "schemaVersion": {
            "value": "1.0",
            "type": "Text"
          },
          "refDeviceModel": {
            "value": "urn:ngsi:DeviceModel:RaspberryPi:d9e7-43cd-9c68-1111",
            "type": "Reference"
          },
          "serialNumber": {
            "value": "123456789",
            "type": "Text"
          },
          "supplierName": {
            "value": "ACME Direct, Inc.",
            "type": "Text"
          },
          "manufacturerCountry": {
            "value": "UK",
            "type": "Text"
          },
          "factory": {
            "value": "56A8",
            "type": "Text"
          },
          "dateManufactured": {
            "value": "2016-08-21T10:18:16Z",
            "type": "DateTime"
          },
          "description": {
            "value": "Thermocouple",
            "type": "Text"
          },
          "owner": {
            "value": [
              "43c46ff2-b0f7-4e4f-838a-adee1c9cae88",
              "ebf421c9-363b-4ed4-97a0-93a6e39786ff"
            ],
            "type": "List"
          },
          "dateInstalled": {
            "value": "2016-08-22T10:18:16Z",
            "type": "DateTime"
          },
          "dateFirstUsed": {
            "value": "2016-08-22T10:18:16Z",
            "type": "DateTime"
          },
          "hardwareVersion": {
            "value": "1.2",
            "type": "Text"
          },
          "firmwareVersion": {
            "value": "2.8.56",
            "type": "Text"
          },
          "softwareVersion": {
            "value": "2.5.11",
            "type": "Text"
          },
          "osVersion": {
            "value": "8.1",
            "type": "Text"
          },
          "supportedProtocol": {
            "value": [
              "HTTP",
              "HTTPS",
              "FTP"
            ],
            "type": "List"
          },
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
          "online": {
            "value": true,
            "type": "Boolean"
          },
          "status": {
            "value": "SC1001",
            "type": "Text"
          },
          "dateLastCalibration": {
            "value": "2016-08-22T10:18:16Z",
            "type": "DateTime"
          },
          "batteryLevel": {
            "value": {
              "value": 0.7
            },
            "type": "ExtQuantitativeValue"
          },
          "value": {
            "value": {
              "value": 1
            },
            "type": "ExtQuantitativeValue"
          }
    }


    print json

    json_bytes = sys.getsizeof(json)
    headers_bytes = sys.getsizeof(headers)
    total = json_bytes + headers_bytes
    print json_bytes,headers_bytes, total

    response = requests.post(url, headers=headers, json=json)
    print(str(response))
    return response

dm_attr1 = "RaspberryPi3B"
dm_attr2 = "xx"
dm_attr3 = "yy"

posttoorion(dm_attr1, dm_attr2, dm_attr3)

