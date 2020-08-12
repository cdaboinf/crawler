"""crawler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from subscribers import views
from webcrawlers import views as crawler_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # get all subscribers
    path('subscribers/', views.subscribers.as_view(), name='subscribers'),
    # get single subscriber
    path('subscribers/<int:id>/', views.subscribers_details.as_view(), name='subscribers_details'),
    # path(r'subscribers/(?P<id>[0-9]+)$', views.subscribers.as_view(), name='subscribers'),
    # get all webcrawlers
    path('webcrawlers/', crawler_views.webcrawlers.as_view(), name='webcrawlers'),
    # get single webcrawlers
    path('webcrawlers/<int:id>/', crawler_views.webcrawlers_details.as_view(), name='webcrawlers_details')
]
