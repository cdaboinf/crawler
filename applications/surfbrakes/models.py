from django.db import models
from django.contrib.postgres.fields import ArrayField

class Surfbrake(models.Model):
    id = models.IntegerField(primary_key=True)
    station = models.ForeignKey('stations.Station', blank=True, on_delete=models.CASCADE)  
    name = models.TextField(max_length=100)
    description = models.EmailField()
    tide = ArrayField(ArrayField(models.DecimalField(blank=True, decimal_places=4, max_digits=10)))
    wind = ArrayField(ArrayField(models.DecimalField(blank=True, decimal_places=4, max_digits=10)))
    wave_height = models.TextField()
    temperature = models.TextField()
    water_temperature = models.TextField()
    rain_posibility = models.TextField()
    summary = models.TextField()
    active = models.BooleanField()
