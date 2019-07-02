from django.core.management.base import BaseCommand
from thermo.models import Record
from datetime import datetime

from django.db.models import Q
import pytz
import requests


class Command(BaseCommand):
    help = 'Retrieves weather data from OpenWeatherMap'

    def handle(self, *args, **options):
        station = {
            'station_id': 17,
            'name': 'Wrocław - Korzeniowskiego',
            'lat:': 51.129378,
            'lon': 17.029250,
            'sensors': [
                {
                    'sensor_id': 665,
                    'param_code': 'NO2'
                },
                {
                    'sensor_id': 667,
                    'param_code': 'O3'
                },
                {
                    'sensor_id': 670,
                    'param_code': 'PM2.5'
                },
                {
                    'sensor_id': 14395,
                    'param_code': 'PM10'
                },
            ],
        }

        api_url = 'http://api.gios.gov.pl/pjp-api/rest/'
        sensor_url = 'data/getData/'
        aqi_url = 'aqindex/getIndex/'

        tz = pytz.timezone('Europe/Warsaw')

        last_record = Record.objects.filter(Q(no2__isnull=False)
                                            | Q(o3__isnull=False)
                                            | Q(pm25__isnull=False)
                                            | Q(pm10__isnull=False)).order_by('date').last()

        if last_record:
            time_diff = datetime.now(pytz.utc) - last_record.date
            if time_diff.total_seconds() / 3600 > 1.75:
                print(time_diff.total_seconds()/3600)

                responses = dict()
                for sensor in station['sensors']:
                    request_url = api_url + sensor_url + str(sensor['sensor_id'])
                    print(request_url)
                    response = requests.get(request_url).json()

                    for element in response['values']:
                        value_datetime = datetime.strptime(element['date'], '%Y-%m-%d %H:%M:%S')
                        value_datetime = tz.normalize(tz.localize(value_datetime)).astimezone(pytz.utc)

                        time_diff = last_record.date - value_datetime

                        if time_diff.total_seconds() / 3600 < 0:
                            value_datetime = value_datetime.replace(minute=0, second=0)

                            if element['value'] is not None:
                                if value_datetime in responses:
                                    responses[value_datetime][sensor['param_code']] = element['value']
                                else:
                                    responses[value_datetime] = {sensor['param_code']: element['value']}

                for key, value in responses.items():
                    if len(value) > 2:
                        if 'NO2' not in value:
                            value['NO2'] = None
                        if 'O3' not in value:
                            value['O3'] = None
                        if 'PM2.5' not in value:
                            value['PM2.5'] = None
                        if 'PM10' not in value:
                            value['PM10'] = None

                        defaults = {
                            'no2': value['NO2'],
                            'o3': value['O3'],
                            'pm25': value['PM2.5'],
                            'pm10': value['PM10']
                        }

                        Record.objects.update_or_create(
                            date=key,
                            defaults=defaults
                        )

        else:
            responses = dict()
            for sensor in station['sensors']:
                request_url = api_url + sensor_url + str(sensor['sensor_id'])
                print(request_url)
                response = requests.get(request_url).json()

                for element in response['values']:
                    value_datetime = datetime.strptime(element['date'], '%Y-%m-%d %H:%M:%S')
                    value_datetime = tz.normalize(tz.localize(value_datetime)).astimezone(pytz.utc)

                    value_datetime = value_datetime.replace(minute=0, second=0)

                    if element['value'] is not None:
                        if value_datetime in responses:
                            responses[value_datetime][sensor['param_code']] = element['value']
                        else:
                            responses[value_datetime] = {sensor['param_code']: element['value']}

            for key, value in responses.items():
                if len(value) > 2:
                    if 'NO2' not in value:
                        value['NO2'] = None
                    if 'O3' not in value:
                        value['O3'] = None
                    if 'PM2.5' not in value:
                        value['PM2.5'] = None
                    if 'PM10' not in value:
                        value['PM10'] = None

                    defaults = {
                        'no2': value['NO2'],
                        'o3': value['O3'],
                        'pm25': value['PM2.5'],
                        'pm10': value['PM10']
                    }

                    Record.objects.update_or_create(
                        date=key,
                        defaults=defaults
                    )
