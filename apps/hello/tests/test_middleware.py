# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test import Client
from apps.hello.models import RequestsLog
from django.core.urlresolvers import reverse


class RequestsMiddlewareTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_middleware_save_requests_in_db(self):
        """Check, if middleware save requests in db"""
        db_content = RequestsLog.objects.exists()
        self.assertEqual(db_content, False)
        self.client.get('/')
        db_content = RequestsLog.objects.all()
        self.assertEqual(len(db_content), 1)
        self.assertEqual(db_content[0].path, '/')

    def test_middleware_dont_save_ajax_requests(self):
        """Check, if middleware don't save ajax requests"""
        db_content = RequestsLog.objects.exists()
        self.assertEqual(db_content, False)
        self.client.get(reverse('hello:requests_page'),
                        {'last_edit_time': ''},
                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        db_content = RequestsLog.objects.exists()
        self.assertEqual(db_content, False)
