from django.core.management.base import BaseCommand, CommandError
from thermo.models import Record
from thermo.views import get_current_reading
from datetime import datetime


class Command(BaseCommand):
    help = 'Retrievs measurement data from the DHT22 sensor and saves it to the database.'

    def handle(self, *args, **options):
        reading = get_current_reading()
        r = Record(date=datetime.now(), indoor_temperature=reading['temperature'], indoor_humidity=reading['humidity'])
        r.save()
