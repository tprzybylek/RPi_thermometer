from django.core.management.base import BaseCommand
from thermo.models import Record
from datetime import datetime

from django.db.models import Q
import pytz
import requests


class Command(BaseCommand):
    help = 'Retrieves weather data from OpenWeatherMap'

    def handle(self, *args, **options):
        def create_record():
            response = requests. \
                get(request_url, params={'id': city_id, 'appid': api_key, 'units': 'metric', 'lang': 'pl'}) \
                .json()

            utc = pytz.utc
            ts = response['dt']
            ts = utc.localize(datetime.utcfromtimestamp(ts)).replace(minute=0, second=0)

            defaults = {
                'outdoor_temperature': response['main']['temp'],
                'outdoor_humidity': response['main']['humidity'],
            }

            Record.objects.update_or_create(
                date=ts,
                defaults=defaults
            )

        api_key = 'df2fbf0c442d4a6319693cb6e72cdb49'
        city_id = '3081368'
        request_url = 'http://api.openweathermap.org/data/2.5/weather'

        last_record = Record.objects.filter(Q(outdoor_temperature__isnull=False)
                                            | Q(outdoor_humidity__isnull=False)).order_by('date').last()

        if last_record:
            time_diff = datetime.now(pytz.utc) - last_record.date
            if time_diff.total_seconds() / 3600 > 1:
                create_record()
        else:
            create_record()
