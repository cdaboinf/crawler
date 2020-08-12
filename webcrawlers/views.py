from django.shortcuts import render
from webcrawlers import models
from django.views import View

import http.client
import re
import json
import datetime

class webcrawlers(View):
    def get(self, request):
        webcrawlers = models.Webcrawler.objects.all()
        
        return render(request, 'webcrawlers/index.html', {'webcrawlers': webcrawlers})

class webcrawlers_details(View):
    def get(self, request, id):
        uid = id
        webcrawler = models.Webcrawler.objects.get(pk=uid)

        return render(request, 'webcrawlers/webcrawler.html', {'webcrawler': webcrawler})
