# -*- coding: utf-8 -*-
from django.test import TestCase
from apps.hello.templatetags import admin_tag
from apps.hello.models import Person


class AdminTagTest(TestCase):

    def test_edit_link_return_proper_url(self):
        any_object = Person.objects.first()
        obj_admin_url = ('/admin/%s/%s/%d/' % (
            any_object._meta.app_label,
            any_object._meta.model_name,
            any_object.id
        ))
        admin_link = admin_tag.edit_link(any_object)
        self.assertEqual(admin_link, obj_admin_url)
