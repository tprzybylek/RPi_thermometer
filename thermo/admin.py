from django.contrib import admin
from .models import Record


class RecordAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'indoor_temperature',
                    'indoor_humidity',
                    'outdoor_temperature',
                    'outdoor_humidity',
                    'no2',
                    'o3',
                    'pm25',
                    'pm10')


admin.site.register(Record, RecordAdmin)
