# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test import Client


class HomePageViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_request_to_home_page_return_correct_status_code(self):
        """Check, if request to home_page return status code 200"""
        test_response = self.client.get('/')
        self.assertEqual(test_response.status_code, 200)

    def test_request_to_edit_page_uses_proper_template(self):
        """Check, if request to home_page right template"""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'hello/home_page.html')
