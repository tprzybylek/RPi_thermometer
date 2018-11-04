from django.shortcuts import render, HttpResponse
from .models import Record
import Adafruit_DHT as adafruit
import random
from datetime import datetime, timedelta
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


def dashboard(request):
    reading = get_current_reading()

    date_from = datetime.now() - timedelta(days=7)

    temperature = Record.objects.filter(date__gte=date_from).values_list('date', 'temperature')
    humidity = Record.objects.filter(date__gte=date_from).values_list('date', 'humidity')

    temperature_json = json.dumps(list(temperature), cls=DjangoJSONEncoder)
    humidity_json = json.dumps(list(humidity), cls=DjangoJSONEncoder)

    reading['records'] = {}

    reading['records']['temperature'] = temperature_json
    reading['records']['humidity'] = humidity_json

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
