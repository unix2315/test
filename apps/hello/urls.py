# -*- coding: utf-8 -*-
from django.conf.urls import url
from apps.hello.views import home_view, requests_view
from django.views.generic.base import TemplateView


urlpatterns = [
    url(r'^$', home_view, name='home_page'),
    url(r'^requests/$', requests_view, name='requests_page'),
    url(r'^edit/$', TemplateView.as_view(template_name="hello/edit_page.html")),
]
