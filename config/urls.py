# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from econadmin import urls

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('servidor.views.home', name='home')),
)