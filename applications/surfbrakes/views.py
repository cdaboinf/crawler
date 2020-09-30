from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from applications.surfbrakes import models
from applications.stations import models as station_models
from decimal import Decimal
from django.forms.models import model_to_dict

import http.client
import re
import json
import datetime

class surfbrakes_surfbrake(View):
    def get(self, request, id):

        # load associted station
        surfbrake = models.Surfbrake.objects.get(pk=id)
        
        # load associted data
        datum = "MLLW"
        product = "predictions"
        units = "english"
        time_zone = "lst"
        format = "json"
        begin_date = "20200929"
        end_date = "20200929"

        # return model
        
        connection = http.client.HTTPSConnection("api.tidesandcurrents.noaa.gov")
        connection.request("GET", f"/api/prod/datagetter?station={surfbrake.station.id}&product={product}&datum={datum}&units={units}&time_zone={time_zone}&format={format}&begin_date={begin_date}&end_date={end_date}")
        response = connection.getresponse()
        content = response.read().decode('utf-8')
        connection.close()

        query_result = json.loads(content)
        predictions_count = len(query_result['predictions'])
        tides = []
        for prediction in query_result['predictions']:
            tides.append(Decimal(prediction['v']))
        
        surfbrake.tide = tides
        return JsonResponse(model_to_dict(surfbrake), safe=False)
