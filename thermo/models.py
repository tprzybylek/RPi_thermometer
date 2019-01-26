from django.db import models


class Record(models.Model):
    date = models.fields.DateTimeField()
    temperature = models.fields.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    humidity = models.fields.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    outdoor_temperature = models.fields.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    outdoor_humidity = models.fields.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    tvoc = models.fields.IntegerField(null=True, blank=True)
    co2 = models.fields.IntegerField(null=True, blank=True)
    aqi = models.fields.IntegerField(null=True, blank=True)
