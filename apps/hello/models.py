# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from PIL import Image
from apps.hello.utils import user_directory_path


class Person(models.Model):
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        null=True
    )
    email = models.EmailField(blank=True)
    skype = models.CharField(max_length=30, blank=True)
    jabber = models.EmailField(blank=True)
    other_contacts = models.TextField(blank=True)

    def __unicode__(self):
        return '%s %s' % (self.name, self.last_name)


class RequestsLog(models.Model):
    request_time = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=6)
    path = models.CharField(max_length=30)
    status_code = models.IntegerField(max_length=3)

    class Meta:
        ordering = ["-request_time"]

    def __unicode__(self):
        return u'%s %s %s' % (self.request_time, self.path, self.method)
