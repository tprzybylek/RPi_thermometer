from django.db import models

class Record(models.Model):
    date = models.fields.DateTimeField()
    temperature = models.fields.DecimalField(max_digits=4, decimal_places=2)
    humidity = models.fields.DecimalField(max_digits=4, decimal_places=2)
