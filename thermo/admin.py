from django.contrib import admin
from .models import Record


class RecordAdmin(admin.ModelAdmin):
    list_display = ('date', 'temperature', 'humidity', 'outdoor_temperature', 'outdoor_humidity', 'aqi')


admin.site.register(Record, RecordAdmin)
