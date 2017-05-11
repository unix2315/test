# -*- coding: utf-8 -*-
from django.conf.urls import url
from apps.hello.views import RequestsView, HomeView
from apps.hello.views import EditView


urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home_page'),
    url(r'^requests/$', RequestsView.as_view(), name='requests_page'),
    url(r'^edit/$', EditView.as_view(), name='edit_page'),
]
