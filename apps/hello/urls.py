# -*- coding: utf-8 -*-
from django.conf.urls import url
from apps.hello.views import home_view
from django.views.generic.base import TemplateView


urlpatterns = [
    url(r'^$', home_view, name='home_page'),
    url(
        r'^requests/$',
        TemplateView.as_view(template_name="hello/requests_page.html"),
        name='requests_page'
    ),
]
