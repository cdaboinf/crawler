from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.http import JsonResponse
from subscribers import models
from django.core import serializers

import http.client
import re
import json
import datetime

class subscribers(View):
    def get(self, request):
        # <view logic>
        user = models.Subscriber(
            id=1,
            name = "Carlos Daboin",
            email = "cedaboin@gmail.com",
            created = datetime.datetime.now(),
            active = True)

        vendor = models.Vendor(
            id = 1,
            created = datetime.datetime.now(),
            subscriber = user,
            site_url = "www.gamestop.com",
            #site_endpoint = "/video-games/switch/consoles",
            site_endpoint = "/video-games/switch/consoles/products/nintendo-switch-with-neon-blue-and-neon-red-joy-con/11095819.html?rt=productDetailsRedesign&utm_expid=.h77-PyHtRYaskNpc14UbmA.1&utm_referrer=https%3A%2F%2Fwww.gamestop.com%2Fvideo-games%2Fswitch%2Fconsoles",
            item = "Nintendo Switch",
            search_object_regex = r"\"offers\":(.|\n)*?\}\]",
            search_object_property_list = "offers",
            search_object_property_availability = "availability"
            )

        connection = http.client.HTTPSConnection(vendor.site_url)
        #connection.request("GET", "/video-games/switch/consoles/products/nintendo-switch-with-neon-blue-and-neon-red-joy-con/11095819.html?rt=productDetailsRedesign&utm_expid=.h77-PyHtRYaskNpc14UbmA.1&utm_referrer=https%3A%2F%2Fwww.gamestop.com%2Fvideo-games%2Fswitch%2Fconsoles")
        connection.request("GET", vendor.site_endpoint)
        response = connection.getresponse()
        content = response.read().decode('utf-8')

        #parsed_value = re.search(r'"offers":(.|\n)*?\}\]', content)
        parsed_value = re.search(vendor.search_object_regex, content)
        value = "{" + parsed_value.group(0) + "}"
        offers = json.loads(value)

        for offer in offers[vendor.search_object_property_list]:
            #for key, value in offer.items():
            offer['site'] = "https://" + vendor.site_url + vendor.site_endpoint
            offer['item'] = vendor.item
            offer['___AVAILABILITY___'] = offer.get(vendor.search_object_property_availability)

        connection.close()

        return JsonResponse(offers)
