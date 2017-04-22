# -*- coding: utf-8 -*-
from django.conf.urls import url
from apps.hello.views import home_view, edit_view
from django.contrib.auth.views import login, logout
from apps.hello.views import RequestsView


urlpatterns = [
    url(r'^$', home_view, name='home_page'),
    # url(r'^requests/$', requests_view, name='requests_page'),
    url(r'^requests/$', RequestsView.as_view(), name='requests_page'),
    url(r'^edit/$', edit_view, name='edit_page'),
    url(r'^login/$', login, name='login'),
    url(
        r'^logout/',
        logout,
        {'next_page': '/'},
        name='logout'
    ),
]
