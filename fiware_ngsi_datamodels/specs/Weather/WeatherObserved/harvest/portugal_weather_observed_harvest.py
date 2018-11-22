#!bin/python
# -*- coding: utf-8 -*-

import argparse
import urllib2
import StringIO
import csv
import datetime
import json
import logging
import logging.handlers
from pytz import timezone
import contextlib
import re

# List of known weather stations
station_data = {}

# Orion service that will store the data
orion_service = 'http://localhost:1030'

logger = None

# Statistics for tracking purposes
persisted_entities = 0
in_error_entities = 0
persisted_stations = 0
total_stations = 0

MIME_JSON = 'application/json'
fiware_service = None
fiware_service_path = None

only_latest = False

stations_to_retrieve_data = []


def decode_wind_direction(direction):
    return {
        '9': 180,  # North
        '5': 0,    # South
        '3': -90,  # East
        '7': 90,   # West
        '2': -135,  # Northeast
        '8': 135,  # Northwest
        '4': -45,  # Southeast
        '6': 45    # Southwest
    }.get(direction, None)


# Sanitize string to avoid forbidden characters by Orion
def sanitize(str_in):
    return re.sub(r"[<(>)\"\'=;-]", "", str_in)


def get_weather_observed_portugal():
    req = urllib2.Request(
        url='http://www.ipma.pt/resources.www/transf/obs-sup/observations.json')
    with contextlib.closing(urllib2.urlopen(req)) as f:
        json_str = f.read()

        source_data = json.loads(json_str)

        # Contains observation data indexed by station code
        observation_data = {}

        for date in source_data:
            for station_code in source_data[date]:
                if len(stations_to_retrieve_data) > 0 and station_code not in stations_to_retrieve_data:
                    continue

                if station_code not in observation_data:
                    observation_data[station_code] = []

                this_station_data = source_data[date][station_code]
                if this_station_data is None:
                    continue

                observation = {
                    'type': 'WeatherObserved',
                    'stationCode': {
                        'value': station_code
                    },
                    'stationName': {
                        'value': sanitize(station_data[station_code]['name'])
                    }
                }

                observation['temperature'] = {
                    'value': get_value(this_station_data['temperatura'])
                }
                observation['windSpeed'] = {
                    'value': get_value(this_station_data['intensidadeVento'])
                }
                observation['windDirection'] = {'value': decode_wind_direction(
                    str(this_station_data['idDireccVento']))}
                observation['precipitation'] = {
                    'value': get_value(this_station_data['precAcumulada'])
                }

                observation['atmosfericPressure'] = {
                    'value': get_value(this_station_data['pressao'])
                }

                observation['relativeHumidity'] = {
                    'value': get_value(this_station_data['humidade'], 100)
                }

                observation['dateObserved'] = {
                    'value': date,
                    'type': 'DateTime'
                }

                observation['source'] = {
                    'value': 'https://www.ipma.pt/',
                    'type': 'URL'
                }
                observation['dataProvider'] = {
                    'value': 'FIWARE'
                }
                observation['location'] = {
                    'value': station_data[station_code]['location'],
                    'type': 'geo:json'
                }

                observation['id'] = 'Portugal-WeatherObserved' + \
                    '-' + station_code + '-' + date

                observation_data[station_code].append(observation)

                # A batch of station data is persisted
                #
    for station_code in observation_data:
        if len(observation_data[station_code]) > 0:
            latest_observation = observation_data[station_code][-1]
            latest_observation['id'] = 'Portugal-WeatherObserved' + \
                '-' + station_code + '-' + 'latest'

        post_station_data_batch(station_code, observation_data[station_code])


def get_value(value, scale=1):
    return None if value < 0 else value / scale

# POST data to an Orion Context Broker instance using NGSIv2 API


def post_station_data_batch(station_code, data):
    if len(data) == 0:
        return

    data_to_be_stored = data

    if only_latest:
        data_to_be_stored = [data[-1]]

    data_obj = {
        'actionType': 'APPEND',
        'entities': data_to_be_stored
    }
    data_as_str = json.dumps(data_obj)

    headers = {
        'Content-Type': MIME_JSON,
        'Content-Length': len(data_as_str)
    }

    if fiware_service:
        headers['Fiware-Service'] = fiware_service

    if fiware_service_path:
        headers['Fiware-Servicepath'] = fiware_service_path

    logger.debug(
        'Going to persist %s (%d) to %s',
        station_code,
        len(data),
        orion_service)

    req = urllib2.Request(
        url=(
            orion_service +
            '/v2/op/update'),
        data=data_as_str,
        headers=headers)

    try:
        with contextlib.closing(urllib2.urlopen(req)) as f:
            global persisted_entities
            global persisted_stations
            persisted_entities = persisted_entities + len(data)
            persisted_stations += 1
            logger.debug('Entities successfully created for station: %s %d/%d',
                         station_code, persisted_stations, total_stations)
    except urllib2.URLError as e:
        logger.error('Error!!! %s', station_code)
        global in_error_entities
        logger.error(
            'Error while POSTing data to Orion: %d %s',
            e.code,
            e.read())
        logger.debug('Data which failed: %s', data_as_str)
        in_error_entities = in_error_entities + 1


# Reads station data from CSV file
def load_station_data():
    req = urllib2.Request(
        url='http://www.ipma.pt/resources.www/transf/obs-sup/stations.json')

    with contextlib.closing(urllib2.urlopen(req)) as f:
        data = json.loads(f.read())

        for station in data:
            station_code = str(station['properties']['idEstacao'])

            station_data[station_code] = {
                'name': sanitize(station['properties']['localEstacao']),
                'location': station['geometry']
            }


def setup_logger():
    global logger

    LOG_FILENAME = 'harvest_weather_observed_portugal.log'

    # Set up a specific logger with our desired output level
    logger = logging.getLogger('WeatherObserved')
    logger.setLevel(logging.DEBUG)

    #  Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler(
        LOG_FILENAME, maxBytes=2000000, backupCount=3)
    formatter = logging.Formatter('%(levelname)s %(asctime)s %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Portugal Weather Observed Harvester')

    parser.add_argument('stations', metavar='stations', type=str, nargs='*',
                        help='Station Codes separated by spaces. ' +
                        'See https://jmcanterafonseca.carto.com/viz/e7ccc6c6-9e5b-11e5-a595-0ef7f98ade21/public_map')
    parser.add_argument('--service', metavar='service',
                        type=str, nargs=1, help='FIWARE Service')
    parser.add_argument('--service-path', metavar='service_path',
                        type=str, nargs=1, help='FIWARE Service Path')
    parser.add_argument('--endpoint', metavar='endpoint',
                        type=str, nargs=1, help='Context Broker end point. Example. http://orion:1030')
    parser.add_argument('--latest', action='store_true',
                        help='Flag to indicate to only harvest the latest observation')

    args = parser.parse_args()

    if args.service:
        fiware_service = args.service[0]

    if args.service_path:
        fiware_service_path = args.service_path[0]

    if args.endpoint:
        orion_service = args.endpoint[0]

    if args.latest:
        print('Only retrieving latest observations')
        only_latest = True

    for s in args.stations:
        stations_to_retrieve_data.append(s)

    setup_logger()

    if len(stations_to_retrieve_data) == 0:
        logger.debug('Retrieving data for all stations ....')
    else:
        logger.debug('Only retrieving data for stations: ' +
                     str(stations_to_retrieve_data))

    load_station_data()

    logger.debug(
        '#### Starting a new harvesting and harmonization cycle ... ####')
    logger.debug(
        'Number of weather stations known: %d', len(
            station_data.keys()))
    total_stations = len(station_data.keys())

    get_weather_observed_portugal()

    logger.debug('Number of entities persisted: %d', persisted_entities)
    logger.debug('Number of stations in error: %d', in_error_entities)
    logger.debug('#### Harvesting cycle finished ... ####')
