from django.db import models

class Webcrawler(models.Model):
    id = models.IntegerField(primary_key=True)
    site_name = models.TextField(max_length=100, default='site-name')
    site_url = models.TextField()
    site_endpoint = models.TextField()
    item = models.TextField(max_length=100)
    availability = models.TextField(max_length=100)
    search_object_regex = models.TextField()
    search_object_value = models.TextField()
    search_object_property_list = models.TextField()
    search_object_property_availability = models.TextField()
    created = models.DateTimeField()
