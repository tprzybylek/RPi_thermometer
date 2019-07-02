from django.core.management.base import BaseCommand, CommandError
from thermo.models import Record
from thermo.views import get_current_reading
from datetime import datetime
import pytz


class Command(BaseCommand):
    help = 'Retrievs measurement data from the DHT22 sensor and saves it to the database.'

    def handle(self, *args, **options):
        reading = get_current_reading()

        utc = pytz.utc
        ts = datetime.utcnow()
        ts = utc.localize(ts).replace(second=0, microsecond=0)

        defaults = {
            'indoor_temperature': reading['temperature'],
            'indoor_humidity': reading['humidity'],
        }

        Record.objects.update_or_create(
            date=ts,
            defaults=defaults
        )
