from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from applications.surfbrakes import models
from applications.stations import models as station_models
from decimal import Decimal
from django.forms.models import model_to_dict
from datetime import datetime, timedelta
from django.core import serializers

import http.client
import re
import json

class surfbrakes_surfbrake(View):
    def get(self, request, id):
        # load associted station
        surfbrake = models.Surfbrake.objects.get(pk=id)
        surf_tides = self.__get_tide_information_from_storage(surfbrake)
        surf_winds = self.__get_wind_information_from_storage(surfbrake)

        if len(surf_tides) < 1 or len(surf_winds) < 1:
            surfbrake = self.__set_surfbrake_from_service(surfbrake, id)
            surf_tides = self.__get_tide_information_from_storage(surfbrake)
            surf_winds = self.__get_wind_information_from_storage(surfbrake)

        result = {}
        result['surfbrake'] = model_to_dict(surfbrake)
        result['tide'] = list(surf_tides)
        result['wind'] = list(surf_winds)

        return JsonResponse(result, safe=False)

    def __set_surfbrake_from_service(self, surfbrake, id): 
        tides = self.__get_tide_information_from_service(surfbrake)

        max_tide = max(tides)
        min_tide = min(tides)
        avg_tide = sum(tides)/len(tides)
        wave = max_tide - min_tide

        tide_summary = []
        tide_summary.append(min_tide)
        tide_summary.append(avg_tide)
        tide_summary.append(max_tide)

        surfbrake.tide = tide_summary

        surfbrake.wave_height = f"{'{0:.2f}'.format(wave)} ft"
        surfbrake.wave_height_max = f"{'{0:.2f}'.format(max_tide)} ft"
        surfbrake.wave_height_min = f"{'{0:.2f}'.format(min_tide)} ft"
        surfbrake.wave_height_avg = f"{'{0:.2f}'.format(avg_tide)} ft"

        surfbrake.water_temperature = self.__get_watertemp_information_from_service(surfbrake)
        surfbrake.temperature = self.__get_watertemp_information_from_service(surfbrake)
        surfbrake.wind = self.__get_wind_information_from_service(surfbrake)

         # summary
        if max_tide < Decimal(3) and avg_tide < Decimal(2):
            surfbrake.summary = "Low"
        elif max_tide > Decimal(3) and avg_tide > Decimal(2) and avg_tide < Decimal(5):
            surfbrake.summary = "Good"
        elif max_tide > Decimal(5) and avg_tide > Decimal(3) and avg_tide < Decimal(6):
            surfbrake.summary = "Excellent"
        elif avg_tide > Decimal(5):
            surfbrake.summary = "Big"
        else:
            surfbrake.summary = "Bad"
        
        surfbrake.save()

        return surfbrake

    def __get_tide_information_from_service(self, surfbrake): 
        query_result = self.__send_request_to_service("predictions", surfbrake)
        
        tides = []
        for prediction in query_result['predictions']:
            try:
                tide = models.SurfTide()
                tide.surfbrake = surfbrake     
                tide.value = Decimal(prediction['v'])
                tide.date = datetime.strptime(prediction['t'], '%Y-%m-%d %H:%M')
                tide.day = datetime.strptime(prediction['t'], '%Y-%m-%d %H:%M')
                tide.save()
                tides.append(tide.value)
            except:
                print(prediction)

        return tides

    def __get_wind_information_from_service(self, surfbrake): 
        query_result = self.__send_request_to_service("wind", surfbrake)
        
        winds = []
        gusts = []
        for data in query_result['data']:
            if not data['s'] or not data['t']:
                print(f"null data value: {data}")
                continue
            try:
                wind = models.SurfWind()
                wind.surfbrake = surfbrake     
                wind.value = Decimal(data['s'])
                wind.date = datetime.strptime(data['t'], '%Y-%m-%d %H:%M')
                wind.day = datetime.strptime(data['t'], '%Y-%m-%d %H:%M')
                wind.save()
                winds.append(wind.value)
                gusts.append(Decimal(data['g']))
            except Exception as e:
                print(f"data value: {data}, exception: {str(e)}")
                
        max_wind = max(winds)
        min_wind = min(winds)
        avg_wind = sum(winds)/len(winds)
        max_wind_gust = max(gusts)
        min_wind_gust = min(gusts)
        avg_wind_gust = sum(gusts)/len(gusts)
        
        wind_summary = []
        wind_summary.append(min_wind)
        wind_summary.append(avg_wind)
        wind_summary.append(max_wind)
  
        wind_summary.append(min_wind_gust)
        wind_summary.append(avg_wind_gust)
        wind_summary.append(max_wind_gust)

        return wind_summary

    def __get_watertemp_information_from_service(self, surfbrake):    
        query_result = self.__send_request_to_service("water_temperature", surfbrake)

        temps = []
        for temp in query_result['data']:
            temps.append(Decimal(temp['v']))

        avg_temp = sum(temps)/len(temps)

        water_temperature = f"{'{0:.2f}'.format(avg_temp)} F"
        return water_temperature

    def __get_airtemp_information_from_service(self, surfbrake): 
        query_result = self.__send_request_to_service("air_temperature", surfbrake)

        temps = []
        for temp in query_result['data']:
            temps.append(Decimal(temp['v']))

        avg_temp = sum(temps)/len(temps)

        air_temperature = f"{'{0:.2f}'.format(avg_temp)} F"
        return air_temperature

    def __send_request_to_service(self, search_product, surfbrake):
        # date query
        local_time = self.__get_local_time()

        # load associted data
        datum = "MLLW"
        units = "english"
        time_zone = "lst"
        format = "json"
        begin_date = local_time.strftime("%Y%m%d")
        end_date = local_time.strftime("%Y%m%d")

        connection = http.client.HTTPSConnection("api.tidesandcurrents.noaa.gov")
        connection.request("GET", f"/api/prod/datagetter?station={surfbrake.station.id}&product={search_product}&datum={datum}&units={units}&time_zone={time_zone}&format={format}&begin_date={begin_date}&end_date={end_date}")
        response = connection.getresponse()
        content = response.read().decode('utf-8')
        query_result = json.loads(content)

        return query_result

    def __get_tide_information_from_storage(self, surfbrake): 
        local_time = self.__get_local_time()
        surf_tides = models.SurfTide.objects.filter(surfbrake=surfbrake).filter(day=local_time.strftime("%Y-%m-%d")).values('value','date')

        return surf_tides
    
    def __get_wind_information_from_storage(self, surfbrake): 
        local_time = self.__get_local_time()
        surf_winds = models.SurfWind.objects.filter(surfbrake=surfbrake).filter(day=local_time.strftime("%Y-%m-%d")).values('value','date')

        return surf_winds

    def __get_local_time(self):
        today = datetime.today()
        local_time = today  - timedelta(hours=5)

        return local_time