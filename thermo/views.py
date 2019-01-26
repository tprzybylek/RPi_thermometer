from django.shortcuts import render, HttpResponse
from .models import Record
import Adafruit_DHT as adafruit
import random
from datetime import datetime, timedelta

import requests

from django.utils import timezone

import ephem

import json
from django.core.serializers.json import DjangoJSONEncoder


def get_current_reading():
    sensor_model = adafruit.AM2302
    sensor_pin = 4

    humidity, temperature = adafruit.read_retry(sensor_model, sensor_pin)
    humidity = round(humidity, 0)
    temperature = round(temperature, 1)

    # humidity, temperature = round(random.uniform(45.0, 80.0), 0), round(random.uniform(15.0, 23.0), 1)

    if humidity and temperature:
        return {'humidity': humidity, 'temperature': temperature}
    else:
        return 'No signal'


def get_air_quality():
    # url_index = 'http://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/'
    # data_url = 'http://api.gios.gov.pl/pjp-api/rest/data/getData/'
    # station_ids = {'Wrocław - Wisniowa': 129, 'Wrocław - Korzeniowskiego': 1064}

    token = '765925262e407136cae60b3c0f81f4042dca5d0d'
    station_ids = [{'id': 8129,
                    'country': 'poland',
                    'region': 'dolnoslaskie',
                    'station_name': 'wroclaw-wisniowa'}]

    for station in station_ids:
        data_url = 'http://api.waqi.info/feed/' \
                   + station['country'] + '/' \
                   + station['region'] + '/' \
                   + station['station_name'] + '/'

        r = requests.get(data_url, params={'token': token})

        print(r.url)
        r = r.json()
        # r = {'status': 'ok', 'data': {'aqi': 134, 'idx': 8129, 'attributions': [
        #     {'url': 'http://powietrze.gios.gov.pl/', 'name': 'Główny inspektorat ochrony środowiska'},
        #     {'url': 'http://www.wroclaw.pios.gov.pl/',
        #      'name': 'Wojewódzki Inspektorat Ochrony Środowiska w Zielonej Górze'},
        #     {'url': 'https://waqi.info/', 'name': 'World Air Quality Index Project'}],
        #                               'city': {'geo': [51.086225, 17.012689], 'name': 'Wrocław - Wiśniowa, Poland',
        #                                        'url': 'https://aqicn.org/city/poland/dolnoslaskie/wroclaw-wisniowa'},
        #                               'dominentpol': 'pm25',
        #                               'iaqi': {'co': {'v': 8.1}, 'h': {'v': 83.3}, 'no2': {'v': 21.8},
        #                                        'p': {'v': 1012.3}, 'pm25': {'v': 134}, 't': {'v': -7.3},
        #                                        'w': {'v': 0.5}, 'wg': {'v': 3.6}},
        #                               'time': {'s': '2019-01-25 18:00:00', 'tz': '+01:00', 'v': 1548439200},
        #                               'debug': {'sync': '2019-01-26T04:47:06+09:00'}}}

        data = dict()
        data['aqi'] = r['data']['aqi']
        data['station'] = r['data']['city']['name']

        dt = datetime.fromtimestamp(int(r['data']['time']['v']))
        data['time'] = dt

        data['outdoor_temperature'] = r['data']['iaqi']['t']['v']

        if 'h' in r['data']['iaqi']:
            data['humidity'] = r['data']['iaqi']['h']['v']
        else:
            data['outdoor_humidity'] = None

        return data


def dashboard(request):
    reading = get_current_reading()

    date_from = datetime.now() - timedelta(hours=24)

    temperature = Record.objects.filter(date__gte=date_from).exclude(temperature=None).values_list('date', 'temperature')
    humidity = Record.objects.filter(date__gte=date_from).exclude(humidity=None).values_list('date', 'humidity')
    outdoor_temperature = Record.objects.filter(date__gte=date_from).exclude(outdoor_temperature=None).values_list('date', 'outdoor_temperature')
    outdoor_humidity = Record.objects.filter(date__gte=date_from).exclude(outdoor_humidity=None).values_list('date', 'outdoor_humidity')
    aqi = Record.objects.filter(date__gte=date_from).exclude(aqi=None).values_list('date', 'aqi')

    temperature_json = json.dumps(list(temperature), cls=DjangoJSONEncoder)
    humidity_json = json.dumps(list(humidity), cls=DjangoJSONEncoder)
    outdoor_temperature_json = json.dumps(list(outdoor_temperature), cls=DjangoJSONEncoder)
    outdoor_humidity_json = json.dumps(list(outdoor_humidity), cls=DjangoJSONEncoder)
    aqi_json = json.dumps(list(aqi), cls=DjangoJSONEncoder)

    reading['records'] = {}

    reading['records']['temperature'] = temperature_json
    reading['records']['humidity'] = humidity_json
    reading['records']['outdoor_temperature'] = outdoor_temperature_json
    reading['records']['outdoor_humidity'] = outdoor_humidity_json
    reading['records']['aqi'] = aqi_json

    reading['outdoor_temperature'] = outdoor_temperature.last()[1]
    reading['outdoor_humidity'] = outdoor_humidity.last()[1]
    reading['aqi'] = aqi.last()[1]

    if reading['aqi']:
        if reading['aqi'] >= 300:
            reading['aqi_level_description'] = 'hazardous'
            reading['aqi_level'] = 5
        elif reading['aqi'] >= 200:
            reading['aqi_level_description'] = 'very unhealthy'
            reading['aqi_level'] = 4
        elif reading['aqi'] >= 150:
            reading['aqi_level_description'] = 'unhealthy'
            reading['aqi_level'] = 3
        elif reading['aqi'] >= 100:
            reading['aqi_level_description'] = 'unhealthy*'
            reading['aqi_level'] = 2
        elif reading['aqi'] >= 50:
            reading['aqi_level_description'] = 'moderate'
            reading['aqi_level'] = 1
        else:
            reading['aqi_level_description'] = 'good'
            reading['aqi_level'] = 0
    else:
        reading['aqi_level_description'] = 'NaN'
        reading['aqi_level'] = 'NaN'

    city = ephem.Observer()
    city.lat = '51.110'
    city.lon = '17.032'
    city.elev = 110
    city.date = datetime.utcnow()

    utc_tz = timezone.utc
    loc_tz = timezone.get_current_timezone()

    sunrise_utc = city.previous_rising(ephem.Sun()).datetime().replace(tzinfo=utc_tz)
    sunset_utc = city.next_setting(ephem.Sun()).datetime().replace(tzinfo=utc_tz)

    sunrise_local = sunrise_utc.astimezone(loc_tz)
    sunset_local = sunset_utc.astimezone(loc_tz)

    reading['sunrise'] = sunrise_local.strftime('%H:%M')
    reading['sunset'] = sunset_local.strftime('%H:%M')

    return render(request, 'thermo/dashboard.html', reading)
