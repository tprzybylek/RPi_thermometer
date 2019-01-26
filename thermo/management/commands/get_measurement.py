from django.core.management.base import BaseCommand, CommandError
from thermo.models import Record
from thermo.views import get_current_reading, get_air_quality
from datetime import datetime


class Command(BaseCommand):
    help = 'Retrievs measurement data from the DHT22 sensor and saves it to the database.'

    def handle(self, *args, **options):
        reading = get_current_reading()
        r = Record(date=datetime.now(), temperature=reading['temperature'], humidity=reading['humidity'])
        r.save()

        reading = get_air_quality()

        if Record.objects.filter(date=reading['time'], aqi=reading['aqi']):
            pass
        else:
            r = Record(date=reading['time'],
                       outdoor_temperature=reading['outdoor_temperature'],
                       outdoor_humidity=reading['outdoor_humidity'],
                       aqi=reading['aqi'])
            r.save()
