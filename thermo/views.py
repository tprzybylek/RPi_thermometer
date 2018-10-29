from django.shortcuts import render, HttpResponse
from .models import records
import Adafruit_Python_DHT as adafruit


def get_current_reading():
    sensor_model = adafruit.AM2302
    sensor_pin = 4

    humidity, temperature = adafruit.read_retry(sensor_model, sensor_pin)

    if humidity and temperature:
        return {'humidity': humidity, 'temperatury': temperature}
    else:
        return 'No signal'


def dashboard(request):
    reading = get_current_reading()

    return render(request, 'thermo/dashboard.html', reading)
