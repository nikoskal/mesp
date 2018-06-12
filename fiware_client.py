import requests
import datetime
import time
import sys

local_url = 'http://localhost:1026'
okeanos_url = 'http://83.212.109.126:1026'

measurments = []
cross_ref_unique_ids = []

experimental_results_list = []

def calltoopenweathermap():
    print("Goodbye, World!")
    weather_url = 'http://api.openweathermap.org/data/2.5/forecast?lat=38.303860&lon=23.730180&cnt=5&appid=3a87a263c645ea5eb18ad7417be4cb0d'
    print weather_url
    response = requests.post(weather_url)
    print response.json()


def getfromorion_id(id):
    print("get from Orion!")
    url = _url + '/v2/entities/' + id
    headers = {'Accept': 'application/json', 'X-Auth-Token': 'QGIrJsK6sSyKfvZvnsza6DlgjSUa8t'}
    # print url
    response = requests.get(url, headers=headers)
    return response.json()


def getfromorion_all():
    print("get from Orion!")
    # payload = {'limit': '500'}
    url = _url + '/v2/entities?limit=500'
    headers = {'Accept': 'application/json', 'X-Auth-Token': 'QGIrJsK6sSyKfvZvnsza6DlgjSUa8t' }
    # print url
    response = requests.get(url, headers=headers)
    # print response.json()
    return response.json()


def load_measurments(data_stream):
    sensed_data_list = []
    try:
        with open(data_stream) as f:
            for line in f:
                key = line.split()
                sensed_data_list.append(key[0])
    except IOError:
        print 'Cannot open file: sensed_data'
        print 'Make sure that negative_list file exists in the same folder as ??.py'

    return sensed_data_list


def posttoorion(snapshot_raw):
    print("parse snapshot")
    print snapshot_raw

    experimental_results = {}
    ts1_received = time.time()
    experimental_results["ts1_received"] = ts1_received

    tokens_dict = snapshot_raw.split(";")
    # print("after tokenisation")
    snapshot = {}

    date = tokens_dict[0].split(":")
    snapshot["date"] = date[1]

    nodeid = tokens_dict[1].split(":")
    snapshot["nodeid"] = nodeid[1]

    _time = tokens_dict[2].split(":")
    snapshot["sensor_time"] = _time[1]

    gps = tokens_dict[3].split(":")
    snapshot["gps"] = gps[1]

    humidity = tokens_dict[4].split(":")
    snapshot["humidity"] = humidity[1]

    flame = tokens_dict[5].split(":")
    snapshot["flame"] = flame[1]

    temperature_air = tokens_dict[6].split(":")
    snapshot["temperature_air"] = temperature_air[1]

    gas = tokens_dict[7].split(":")
    snapshot["gas"] = gas[1]

    temp_soil = tokens_dict[8].split(":")
    snapshot["temp_soil"] = temp_soil[1]

    print("Post to Orion!")
    print snapshot
    # print("TIME")
    pts = datetime.datetime.now().strftime('%s')
    # print(pts)


    # url = 'http://orion.lab.fiware.org:1026/v2/entities/2107722425'
    url = _url + '/v2/entities'
    headers = {'Accept': 'application/json', 'X-Auth-Token': 'QGIrJsK6sSyKfvZvnsza6DlgjSUa8t'}
    # print url

    json = {

        "id": str(pts),
        "type": "Sensor123",
        "nodeid": {
            "value": snapshot["nodeid"],
            "type": "id"
        },
        "translation_timestamp": {
            "value": str(pts),
            "type": "time"
        },
        "sensor_time": {
            "value":snapshot["sensor_time"],
            "type":"time"
        },
        "gps_location": {
            "value": snapshot["gps"],
            "type": "GPS"
        },
        "humidity": {
            "value": snapshot["humidity"],
            "type": "Number"
        },
        "flame": {
            "value": snapshot["flame"],
            "type": "Number"
        },
        "temperature_air": {
            "value": snapshot["temperature_air"],
            "type": "Number"
        },
        "gas": {
            "value": snapshot["gas"],
            "type": "Number"
        },
        "temp_soil": {
            "value": snapshot["temp_soil"],
            "type": "Number"
        }
    }
    ts2 = time.time()
    print json
    # print "posting"

    translation_time = ts2-ts1_received
    volume = sys.getsizeof(json)
    print "translation time"
    print "entity id, volume, translation_time"
    print str(pts), volume, translation_time

    response = requests.post(url, headers=headers, json=json)

    print "response"
    print(response.text)
    cross_ref_unique_ids.append(str(pts))
    print("list of ids translated and send:")
    print(str(pts))


def post_all(measurments_list):
    print "reading measurment"
    for measurment_one in measurments_list:
        time.sleep(1)
        print measurment_one
        print "posting"
        posttoorion(measurment_one)
        print "done"

    print "finished"


def retrieve_id():
    for id in cross_ref_unique_ids:
        print "retrieving : " + str(id)
        res = getfromorion_id(id)
        print res['id']
        if res['id'] == id:
            print "found"
        else:
            print "not found"


if __name__ == "__main__":

    if(sys.argv[1] != 'local'):
        _url = local_url
    else:
        _url = okeanos_url
    # load measurments from file (1sec interval)
    values = load_measurments(sys.argv[2])
    #
    post_all(values)
    # print("cross_ref_unique_ids")
    print cross_ref_unique_ids


    # retrieve_id()

    # all = getfromorion_all()
    # print len(all)
