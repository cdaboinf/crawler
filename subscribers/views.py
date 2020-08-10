from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.http import JsonResponse
from subscribers import models
from webcrawlers.models import Webcrawler
from django.core import serializers

import http.client
import re
import json
import datetime

class subscribers(View):
    def get(self, request):
        users = models.Subscriber.objects.all()
        
        return render(request, 'subscribers/index.html', {'subscribers': users})

class subscribers_details(View):
    def get(self, request, id):
        uid = id
        user = models.Subscriber.objects.get(pk=uid)

        return render(request, 'subscribers/subscriber.html', {'subscriber': user})
