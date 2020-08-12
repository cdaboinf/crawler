from django.db import models

class Subscriber(models.Model):
    id = models.IntegerField(primary_key=True)
    webcrawlers = models.ManyToManyField('webcrawlers.Webcrawler', blank=True)
    name = models.TextField(max_length=100)
    email = models.EmailField()
    created = models.DateTimeField()
    active = models.BooleanField()