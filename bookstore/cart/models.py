from django.db import models

# Create your models here.
class ClientLocation(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()