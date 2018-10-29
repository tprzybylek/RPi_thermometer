from django.db import models

class records(models.Model):
    date = models.fields.DateTimeField()
    temperature = models.fields.DecimalField(max_digits=3, decimal_places=2)
    humidity = models.fields.DecimalField(max_digits=3, decimal_places=2)
