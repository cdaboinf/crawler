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
    wave_height_max = models.TextField(blank=True, null=True)
    wave_height_min = models.TextField(blank=True, null=True)
    wave_height_avg = models.TextField(blank=True, null=True)
    temperature = models.TextField()
    water_temperature = models.TextField()
    rain_posibility = models.TextField()
    summary = models.TextField()
    active = models.BooleanField()

class SurfTide(models.Model):
    id = models.AutoField(primary_key=True)
    surfbrake = models.ForeignKey('Surfbrake', blank=True, on_delete=models.CASCADE)
    value = models.DecimalField(blank=True, decimal_places=2, max_digits=4)
    date = models.DateTimeField()
    day = models.DateField(blank=True, null=True)

class SurfWind(models.Model):
    id = models.AutoField(primary_key=True)
    surfbrake = models.ForeignKey('Surfbrake', blank=True, on_delete=models.CASCADE)
    value = models.DecimalField(blank=True, decimal_places=2, max_digits=4)
    date = models.DateTimeField()
    day = models.DateField(blank=True, null=True)