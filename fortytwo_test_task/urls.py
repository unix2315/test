# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import logout, login
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'', include('apps.hello.urls', namespace='hello')),
    url(r'^test/', include('apps.chatserver.urls', namespace='chatserver')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login, name='login'),
    url(
        r'^logout/',
        logout,
        {'next_page': '/'},
        name='logout'
    ),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
