from django.db import models

class Subscriber(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(max_length=100)
    email = models.EmailField()
    created = models.DateTimeField()
    active = models.BooleanField()

class Vendor(models.Model):
    id = models.IntegerField(primary_key=True)
    subscriber = models.ForeignKey('Subscriber', on_delete=models.CASCADE)
    site_url = models.TextField()
    site_endpoint = models.TextField()
    item = models.TextField(max_length=100)
    availability = models.TextField(max_length=100)
    search_object_regex = models.TextField()
    search_object_value = models.TextField()
    search_object_property_list = models.TextField()
    search_object_property_availability = models.TextField()
    created = models.DateTimeField()
