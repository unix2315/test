# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True)
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    skype = models.CharField(max_length=30, blank=True)
    jabber = models.EmailField(blank=True)
    other_contacts = models.TextField(blank=True)

    def __unicode__(self):
        return '%s %s' % (self.name, self.last_name)
