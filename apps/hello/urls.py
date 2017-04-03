# -*- coding: utf-8 -*-
from django.conf.urls import url
from apps.hello.views import home_view


urlpatterns = [
    url(r'^$', home_view, name='home_page'),
]
