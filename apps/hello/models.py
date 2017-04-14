# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from apps.hello.utils import user_directory_path, resize_photo
from apps.hello.utils import remove_unused_photo
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


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

    def save(self, *args, **kwargs):
        try:
            exist_person = Person.objects.get(id=self.id)
        except Exception:
            pass
        else:
            remove_unused_photo(self, exist_person)
        super(Person, self).save(*args, **kwargs)
        if self.photo:
            resize_photo(self)


class RequestsLog(models.Model):
    request_time = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=6)
    path = models.CharField(max_length=30)
    status_code = models.IntegerField(max_length=3)

    class Meta:
        ordering = ["-request_time"]

    def __unicode__(self):
        return u'%s %s %s' % (self.request_time, self.path, self.method)


class ModelsLog(models.Model):
    EDIT_ACTIONS = (
        ('ADD', 'Creation'),
        ('EDIT', 'EDIT'),
        ('DEL', 'DELETE'),
    )
    log_time = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=4, choices=EDIT_ACTIONS)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    report = models.CharField(max_length=50, default='')
