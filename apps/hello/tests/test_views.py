# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test import Client
from django.test import RequestFactory
from apps.hello.views import home_view, requests_view
from datetime import date
from apps.hello.models import Person, RequestsLog
import json
from django.core.urlresolvers import reverse
import time


PERSON_DATA = {
    'name': 'Alex',
    'last_name': 'Ivanov',
    'date_of_birth': date(1945, 5, 9)
}

REQUEST_DATA = {
    'method': 'GET',
    'path': '/requests/',
    'status_code': 200
}


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

    def test_home_view_return_correct_status_code(self):
        """Check, if home_view return status code 200"""
        test_request = RequestFactory().get(reverse('hello:home_page'))
        test_response = home_view(test_request)
        self.assertEqual(test_response.status_code, 200)

    def test_home_view_return_proper_model_instance(self):
        """Check, if home view return proper model
        instance in context"""
        test_response = self.client.get(reverse('hello:home_page'))
        self.assertIsInstance(test_response.context['person'], Person)

    def test_home_view_return_proper_person_data(self):
        """Check, if home view response contain proper person data"""
        test_person = Person.objects.first()
        test_response = self.client.get(reverse('hello:home_page'))
        self.assertContains(test_response,
                            test_person.name and
                            test_person.last_name)

    def test_home_view_return_proper_person(self):
        """Check, if the home_view function return proper person,
        if one more person present in DB"""
        test_person = Person(**PERSON_DATA)
        test_person.save()
        proper_person = Person.objects.first()
        test_response = self.client.get(reverse('hello:home_page'))
        self.assertEqual(test_response.context['person'], proper_person)
        self.assertNotEqual(test_response.context['person'], test_person)
        self.assertContains(test_response, proper_person.name)

    def test_home_view_no_data_in_db(self):
        """Check, if home_view return proper message,
        when no data in Person model"""
        Person.objects.all().delete()
        test_response = self.client.get(reverse('hello:home_page'))
        self.assertEqual(test_response.context['person'], None)
        self.assertContains(test_response, "No person was found")


class RequestsViewTest(TestCase):

    def test_request_page_return_correct_status_code(self):
        """Check, if request to requests_page return status code 200"""
        test_response = self.client.get(reverse('hello:requests_page'))
        self.assertEqual(test_response.status_code, 200)

    def test_requests_page_uses_proper_template(self):
        """Check, if home_page view render right template"""
        test_response = self.client.get(reverse('hello:requests_page'))
        self.assertTemplateUsed(test_response, 'hello/requests_page.html')

    def test_requests_view_return_correct_status_code(self):
        """Check, if requests_view return status code 200"""
        test_request = RequestFactory().get(reverse('hello:requests_page'))
        test_response = requests_view(test_request)
        self.assertEqual(test_response.status_code, 200)

    def test_requests_view_return_proper_model_instance(self):
        """Check, if requests view return proper model
        instance in context"""
        test_response = self.client.get(reverse('hello:requests_page'))
        for req in test_response.context['requests']:
            self.assertIsInstance(req, RequestsLog)

    def test_requests_view_without_data_in_db(self):
        """Check, if view return correct status, when no data in model"""
        test_response = self.client.get(reverse('hello:requests_page'))
        self.assertContains(test_response, "No requests was found")

    def test_requests_view_return_only_last_ten_requests(self):
        """Check, if requests_view return only last ten requests"""
        for i in range(20):
            RequestsLog(**REQUEST_DATA).save()
        test_response = self.client.get(reverse('hello:requests_page'))
        self.assertEqual(len(test_response.context['requests']), 10)
        self.assertContains(test_response, '/requests/', count=10)

    def test_requests_view_return_requests_in_proper_order(self):
        """Check, if requests_view return requests
        in proper ordering by time"""
        for i in range(20):
            RequestsLog(**REQUEST_DATA).save()
        last_request = RequestsLog.objects.first()
        test_response = self.client.get(reverse('hello:requests_page'))
        self.assertEqual(test_response.context['requests'][0], last_request)

    def test_ajax_requests_view_return_ten_last_requests(self):
        """Check, if ajax request return last ten requests"""
        for i in range(20):
            RequestsLog(**REQUEST_DATA).save()
        test_response = self.client.get(reverse('hello:requests_page'),
                                        {'last_request_time': ''},
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        ajax_response = json.loads(test_response.content)
        self.assertEqual(len(ajax_response), 10)

    def test_ajax_requests_view_proper_number_of_requests(self):
        """
        Check, if ajax request return only requests,
        with request_time more than last_request_time parameter
        """
        for i in range(20):
            RequestsLog(**REQUEST_DATA).save()
            time.sleep(0.01)
        last_requests = RequestsLog.objects.all()
        third_last_request = last_requests[2].request_time
        test_response = self.client.get(
            reverse('hello:requests_page'),
            {'last_request_time': third_last_request},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        ajax_response = json.loads(test_response.content)
        self.assertEqual(len(ajax_response), 2)

        
class EditPageViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        
    def test_request_to_edit_page_return_correct_status_code(self):
        """Check, if request to edit_page return status code 200"""
        test_response = self.client.get('/edit/')
        self.assertEqual(test_response.status_code, 200)

    def test_request_to_edit_page_uses_proper_template(self):
        """Check, if edit_page view render right template"""
        test_response = self.client.get('/edit/')
        self.assertTemplateUsed(test_response, 'hello/edit_page.html')

    def test_edit_view_return_correct_status_code(self):
        """Check, if edit_view return status code 200"""
        test_request = RequestFactory().get(reverse('hello:edit_page'))
        test_response = edit_view(test_request)
        self.assertEqual(test_response.status_code, 200)
