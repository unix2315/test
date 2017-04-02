# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test import Client
from django.test import RequestFactory
from apps.hello.views import home_view
from django.core.urlresolvers import reverse
from datetime import date
from apps.hello.models import Person


PERSON_DATA = {
    'name': 'Alex',
    'last_name': 'Ivanov',
    'date_of_birth': date(1945, 5, 9)
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
        """Check, if edit_view return status code 200"""
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
