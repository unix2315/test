# -*- coding: utf-8 -*-
from django.conf.urls import url
from apps.hello.views import home_view, requests_view, edit_view


urlpatterns = [
    url(r'^$', home_view, name='home_page'),
    url(r'^requests/$', requests_view, name='requests_page'),
    url(r'^edit/$', edit_view, name='edit_page')
]
