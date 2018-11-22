#!bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from flask import Flask, jsonify, request, Response
import urllib2
import xml.dom.minidom
import datetime
import json
import copy
from dateutil import parser
import csv
import StringIO
import re
from meteoalarm import get_weather_alarms
from ipma import get_weather_forecasted_pt
from weather_observed import get_weather_observed

postal_codes = {
    '47001': '47186',
    '28001': '28079',
    '39001': '39075',
    '34001': '34120',
    '34200': '34023',
    '05194': '05123',
    '33300': '33076',
    '41001': '41091',
    '46005': '46250'
}

localities = {
    'Valladolid': '47186',
    'Madrid': '28079',
    'Santander': '39075',
    'Palencia': '34120',
    u'Venta de Baños': '34023',
    'Mediana de Voltoya': '05123',
    'Villaviciosa': '33076',
    'Sevilla': '41091',
    'Valencia': '46250'
}

app = Flask(__name__)

aemet_service = "http://www.aemet.es/xml/municipios/localidad_{}.xml"


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/v2/entities', methods=['GET'])
def get_weather():
    func = {
        'WeatherForecast': get_weather_forecasted,
        'WeatherObserved': get_weather_observed,
        'WeatherAlarm': get_weather_alarms
    }.get(request.args.get('type'))
    if func:
        return func(request)
    else:
        return Response(json.dumps([]), mimetype='application/json')


def get_data(row, index, conversion=float, factor=1.0):
    value = row[index]
    return None if value == '' else conversion(value) / factor


def get_weather_forecasted(request):
    country = ''
    postal_code = ''
    address_locality = ''

    query = request.args.get('q')

    if not query:
        return Response(json.dumps([]), mimetype='application/json')

    tokens = query.split(';')
    for token in tokens:
        items = token.split(':')
        if items[0] == 'postalCode':
            postal_code = items[1]
        elif items[0] == 'country':
            country = items[1]
        elif items[0] == 'addressLocality':
            address_locality = items[1]

    if country == 'PT' and address_locality:
        return Response(
            json.dumps(
                get_weather_forecasted_pt(address_locality)),
            mimetype='application/json')

    if not country or (
            postal_code in postal_codes and not address_locality not in localities) or country != 'ES':
        return Response(json.dumps([]), mimetype='application/json')

    param = ''
    if postal_code:
        param = postal_codes[postal_code]
    elif address_locality:
        param = localities[address_locality]

    source = aemet_service.format(param)
    req = urllib2.Request(url=source)
    f = urllib2.urlopen(req)
    xml_data = f.read()
    DOMTree = xml.dom.minidom.parseString(xml_data).documentElement

    address_locality = DOMTree.getElementsByTagName(
        'nombre')[0].firstChild.nodeValue
    address = {
        'addressCountry': country,
        'postalCode': postal_code,
        'addressLocality': address_locality
    }

    created = DOMTree.getElementsByTagName('elaborado')[0].firstChild.nodeValue

    forecasts = DOMTree.getElementsByTagName(
        'prediccion')[0].getElementsByTagName('dia')

    out = []
    for forecast in forecasts:
        date = forecast.getAttribute('fecha')
        normalizedForecast = parse_aemet_forecast(forecast, date)
        for i, f in enumerate(normalizedForecast):
            f['type'] = 'WeatherForecast'
            f['id'] = generate_id(
                postal_code, country, date) + '_' + str(i + 1)
            f['address'] = address
            f['dateCreated'] = created
            f['source'] = source
            out.append(f)

    return Response(json.dumps(out), mimetype='application/json')


def parse_aemet_forecast(forecast, date):
    periods = {}
    out = []

    parsed_date = parser.parse(date)

    pops = forecast.getElementsByTagName('prob_precipitacion')
    for pop in pops:
        period = pop.getAttribute('periodo') or '00-24'
        if pop.firstChild and pop.firstChild.nodeValue:
            insert_into_period(
                periods, period, 'precipitationProbability', float(
                    pop.firstChild.nodeValue) / 100.0)

    period = None
    weather_types = forecast.getElementsByTagName('estado_cielo')
    for weather_type in weather_types:
        period = weather_type.getAttribute('periodo') or '00-24'
        if weather_type.firstChild and weather_type.firstChild.nodeValue:
            insert_into_period(periods, period, 'weatherType',
                               weather_type.getAttribute('descripcion'))

    period = None
    wind_data = forecast.getElementsByTagName('viento')
    for wind in wind_data:
        period = wind.getAttribute('periodo') or '00-24'
        wind_direction = wind.getElementsByTagName('direccion')[0]
        wind_speed = wind.getElementsByTagName('velocidad')[0]
        if wind_speed.firstChild and wind_speed.firstChild.nodeValue:
            insert_into_period(periods, period, 'windSpeed',
                               int(wind_speed.firstChild.nodeValue))
        if wind_direction.firstChild and wind_direction.firstChild.nodeValue:
            insert_into_period(periods, period, 'windDirection',
                               wind_direction.firstChild.nodeValue)

    temperature_node = forecast.getElementsByTagName('temperatura')[0]
    max_temp = float(temperature_node.getElementsByTagName(
        'maxima')[0].firstChild.nodeValue)
    min_temp = float(temperature_node.getElementsByTagName(
        'minima')[0].firstChild.nodeValue)
    get_parameter_data(temperature_node, periods, 'temperature')

    temp_feels_node = forecast.getElementsByTagName('sens_termica')[0]
    max_temp_feels = float(temp_feels_node.getElementsByTagName(
        'maxima')[0].firstChild.nodeValue)
    min_temp_feels = float(temp_feels_node.getElementsByTagName(
        'minima')[0].firstChild.nodeValue)
    get_parameter_data(temp_feels_node, periods, 'feelsLikeTemperature')

    humidity_node = forecast.getElementsByTagName('humedad_relativa')[0]
    max_humidity = float(humidity_node.getElementsByTagName(
        'maxima')[0].firstChild.nodeValue) / 100.0
    min_humidity = float(humidity_node.getElementsByTagName(
        'minima')[0].firstChild.nodeValue) / 100.0
    get_parameter_data(humidity_node, periods, 'relativeHumidity', 100.0)

    for period in periods:
        print(period)

    for period in periods:
        period_start, period_end = period.split('-')[:2]
        end_hour = int(period_end)
        end_date = copy.deepcopy(parsed_date)
        if end_hour > 23:
            end_hour = 0
            end_date = parsed_date + datetime.timedelta(days=1)

        start_date = parsed_date.replace(
            hour=int(period_start), minute=0, second=0)
        end_date = end_date.replace(hour=end_hour, minute=0, second=0)

        objPeriod = periods[period]
        objPeriod['validity'] = {
            'from': start_date.isoformat(),
            'to': end_date.isoformat()
        }
        objPeriod['dayMaximum'] = {
            'temperature': max_temp,
            'relativeHumidity': max_humidity,
            'feelsLikeTemperature': max_temp_feels
        }
        objPeriod['dayMinimum'] = {
            'temperature': min_temp,
            'relativeHumidity': min_humidity,
            'feelsLikeTemperature': min_temp_feels
        }
        out.append(objPeriod)

    return out


def get_parameter_data(node, periods, parameter, factor=1.0):
    param_periods = node.getElementsByTagName('dato')
    for param in param_periods:
        hour = int(param.getAttribute('hora'))
        interval_start = hour - 6
        period = '{:02}-{:02}'.format(interval_start, hour)
        if param.firstChild and param.firstChild.nodeValue:
            param_val = float(param.firstChild.nodeValue)
            insert_into_period(periods, period, parameter, param_val / factor)


def insert_into_period(periods, period, attribute, value):
    if period not in periods:
        periods[period] = {}
    periods[period][attribute] = value


def generate_id(postal_code, country, date):
    return '_'.join(postal_code, country, date)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1028, debug=True)
