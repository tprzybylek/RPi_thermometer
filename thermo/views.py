from django.shortcuts import render
from .models import Record
import Adafruit_DHT as adafruit
from datetime import datetime, timedelta
import pytz

import ephem

import json
from django.core.serializers.json import DjangoJSONEncoder


def get_current_reading():
    sensor_model = adafruit.AM2302
    sensor_pin = 4

    humidity, temperature = adafruit.read_retry(sensor_model, sensor_pin)
    humidity = round(humidity, 0)
    temperature = round(temperature, 1)

    if humidity and temperature:
        return {'humidity': humidity, 'temperature': temperature}
    else:
        return None


def dashboard(request):
    reading = dict()
    reading['indoor'] = get_current_reading()

    date_from = datetime.utcnow() - timedelta(hours=24)

    records = Record.objects.filter(date__gte=date_from).order_by('date').values()
    records_list = []

    for record in list(records):
        records_list.append({k: v for k, v in record.items() if v is not None})
    reading['chart_data'] = json.dumps(records_list, cls=DjangoJSONEncoder)

    if records:
        reading['outdoor'] = {}
        if records.exclude(outdoor_temperature=None).last():
            reading['outdoor']['temperature'] = records.exclude(outdoor_temperature=None).last()['outdoor_temperature']
        else:
            reading['outdoor']['temperature'] = None
        if records.exclude(outdoor_humidity=None).last():
            reading['outdoor']['humidity'] = records.exclude(outdoor_humidity=None).last()['outdoor_humidity']
        else:
            reading['outdoor']['humidity'] = None

        reading['aqi'] = {}
        reading['aqi']['index'] = {}
        reading['aqi']['index']['value'] = None
        reading['aqi']['index']['description'] = None

        if records.exclude(pm25=None).last():
            reading['aqi']['PM25'] = records.exclude(pm25=None).last()['pm25']
        else:
            reading['aqi']['PM25'] = None

        if records.exclude(pm10=None).last():
            reading['aqi']['PM10'] = records.exclude(pm10=None).last()['pm10']
        else:
            reading['aqi']['PM10'] = None

        if records.exclude(no2=None).last():
            reading['aqi']['NO2'] = records.exclude(no2=None).last()['no2']
        else:
            reading['aqi']['NO2'] = None

        if records.exclude(o3=None).last():
            reading['aqi']['O3'] = records.exclude(o3=None).last()['o3']
        else:
            reading['aqi']['O3'] = None
    else:
        reading['outdoor'] = {}
        reading['outdoor']['temperature'] = None
        reading['outdoor']['humidity'] = None

        reading['aqi'] = {}
        reading['aqi']['index'] = {}
        reading['aqi']['index']['value'] = None
        reading['aqi']['index']['description'] = None

        reading['aqi']['PM25'] = None
        reading['aqi']['PM10'] = None
        reading['aqi']['NO2'] = None
        reading['aqi']['O3'] = None

    city = ephem.Observer()
    city.lat = '51.110'
    city.lon = '17.032'
    city.elev = 110
    city.date = datetime.utcnow()

    tz = pytz.timezone('Europe/Warsaw')
    sunrise = city.previous_rising(ephem.Sun()).datetime().astimezone(tz)
    sunset = city.next_setting(ephem.Sun()).datetime().astimezone(tz)

    reading['sunrise'] = sunrise.strftime('%H:%M')
    reading['sunset'] = sunset.strftime('%H:%M')

    return render(request, 'thermo/dashboard.html', reading)
