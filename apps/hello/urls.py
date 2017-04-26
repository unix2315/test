# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.views import login, logout
from apps.hello.views import RequestsView, HomeView
from apps.hello.views import EditView


urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home_page'),
    url(r'^requests/$', RequestsView.as_view(), name='requests_page'),
    # url(r'^edit/$', edit_view, name='edit_page'),
    # url(r'^edit/(?P<pk>\d+)/$', EditView.as_view(), name='edit_page'),
    url(r'^edit/$', EditView.as_view(), name='edit_page'),
    url(r'^login/$', login, name='login'),
    url(
        r'^logout/',
        logout,
        {'next_page': '/'},
        name='logout'
    ),
]
