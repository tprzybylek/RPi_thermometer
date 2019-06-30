from django.db import models
from datetime import datetime


class Record(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['date', ])
        ]

    def __str__(self):
        return self.date.strftime('%Y-%m-%d %H:%M:%S%z')

    date = models.fields.DateTimeField(primary_key=True)
    indoor_temperature = models.fields.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    indoor_humidity = models.fields.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    outdoor_temperature = models.fields.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    outdoor_humidity = models.fields.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    tvoc = models.fields.IntegerField(null=True, blank=True)
    aqi = models.fields.IntegerField(null=True, blank=True)
    no2 = models.fields.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    o3 = models.fields.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    pm25 = models.fields.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    pm10 = models.fields.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
