# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test import Client
from django.test import RequestFactory
from apps.hello.views import home_view, requests_view, edit_view
from datetime import date
from apps.hello.models import Person, RequestsLog
from apps.hello.forms import EditForm
import json
from django.core.urlresolvers import reverse
import time
from django.contrib.auth.models import User, AnonymousUser


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

VALID_DATA = {
    'name': 'Alex',
    'last_name': 'Ivanov',
    'date_of_birth': '1945-05-09'
}

INVALID_DATA = {
    'name': '',
    'last_name': '',
    'date_of_birth': '1945'
}

PRIORITY_DATA = {
    '10': 4,
    '9': 3,
    '8': 2
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

    def test_requests_view_return_last_edit_time_in_context(self):
        """Check, if requests_view return last edit time value in context"""
        for i in range(20):
            RequestsLog(**REQUEST_DATA).save()
        db_last_edit_time = (
            RequestsLog
            .objects
            .order_by('edit_time')
            .last()
        )
        test_response = self.client.get(reverse('hello:requests_page'))
        self.assertTrue(test_response.context['last_edit_req'])
        self.assertEqual(
            test_response.context['last_edit_req'].edit_time,
            db_last_edit_time.edit_time
        )

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
                                        {'last_edit_time': ''},
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        ajax_response = json.loads(test_response.content)
        self.assertEqual(len(ajax_response['ajaxReqArr']), 10)

    def test_ajax_requests_view_if_db_has_changed(self):
        """
        Check, if ajax request return last ten requests,
        if data in db has changed,
        and last_edit_time parameter in request,
        less then one in DB
        """
        for i in range(20):
            RequestsLog(**REQUEST_DATA).save()
            time.sleep(0.01)
        last_requests = RequestsLog.objects.all()
        third_last_request = last_requests[2].edit_time
        test_response = self.client.get(
            reverse('hello:requests_page'),
            {'last_edit_time': third_last_request},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        ajax_response = json.loads(test_response.content)
        self.assertEqual(len(ajax_response['ajaxReqArr']), 10)

    def test_ajax_requests_view_if_db_has_no_changes(self):
        """
        Check, if ajax request return empty context,
        if data in db has no changes,
        and last_edit_time parameter in request,
        equal to one in DB
        """
        for i in range(20):
            RequestsLog(**REQUEST_DATA).save()
            time.sleep(0.01)
        db_last_edit_time = (
            RequestsLog
            .objects
            .order_by('edit_time')
            .last()
        ).edit_time
        test_response = self.client.get(
            reverse('hello:requests_page'),
            {'last_edit_time': db_last_edit_time},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        ajax_response = json.loads(test_response.content)
        self.assertEqual(ajax_response, {})

    def test_requests_page_post_request(self):
        """Check, if post request to requests page,
        return last ten requests from db"""
        for i in range(10):
            RequestsLog(**REQUEST_DATA).save()
            time.sleep(0.01)
        test_response = self.client.post(
            reverse('hello:requests_page'),
            PRIORITY_DATA
        )
        self.assertEqual(len(test_response.context['requests']), 10)
        self.assertContains(test_response, '/requests/', count=10)

    def test_requests_page_post_request_change_db(self):
        """Check, if post request to requests page,
        is modify priority field in db"""
        for i in range(10):
            RequestsLog(**REQUEST_DATA).save()
            time.sleep(0.01)
        for req_id in PRIORITY_DATA:
            self.assertNotEqual(
                PRIORITY_DATA[req_id],
                RequestsLog
                .objects
                .get(id=req_id)
                .priority
            )
        self.client.post(
            reverse('hello:requests_page'),
            PRIORITY_DATA
        )
        for req_id in PRIORITY_DATA:
            self.assertEqual(
                PRIORITY_DATA[req_id],
                RequestsLog
                .objects
                .get(id=req_id)
                .priority
            )

    def test_requests_page_ajax_post_request(self):
        """Check, if post ajax request to requests page,
        return last ten requests from db"""
        for i in range(10):
            RequestsLog(**REQUEST_DATA).save()
            time.sleep(0.01)
        test_response = self.client.post(
            reverse('hello:requests_page'),
            PRIORITY_DATA,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        ajax_response = json.loads(test_response.content)
        self.assertEqual(len(ajax_response['ajaxReqArr']), 10)

    def test_requests_page_ajax_post_request_change_db(self):
        """Check, if ajax post request to requests page,
        is modify priority field in db"""
        for i in range(10):
            RequestsLog(**REQUEST_DATA).save()
            time.sleep(0.01)
        for req_id in PRIORITY_DATA:
            self.assertNotEqual(
                PRIORITY_DATA[req_id],
                RequestsLog
                .objects
                .get(id=req_id)
                .priority
            )
        self.client.post(
            reverse('hello:requests_page'),
            PRIORITY_DATA,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        for req_id in PRIORITY_DATA:
            self.assertEqual(
                PRIORITY_DATA[req_id],
                RequestsLog
                .objects
                .get(id=req_id)
                .priority
            )


class EditPageViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.client.login(username='admin', password='admin')

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
        self.admin = User.objects.get(pk=1)
        test_request = RequestFactory().get(reverse('hello:edit_page'))
        test_request.user = self.admin
        test_response = edit_view(test_request)
        self.assertEqual(test_response.status_code, 200)

    def test_edit_page_uses_EditForm(self):
        """Check, if edit_view is return EditForm instance"""
        test_response = self.client.get(reverse('hello:edit_page'))
        self.assertIsInstance(test_response.context['form'], EditForm)

    def test_edit_view_displays_EditForm(self):
        """Check, if proper html of EditForm contains in edit_page"""
        test_response = self.client.get(reverse('hello:edit_page'))
        self.assertContains(test_response, 'form-control', count=8)
        self.assertContains(
            test_response,
            'for="id_name"' and 'id="id_name"'
        )
        self.assertContains(
            test_response,
            'for="name"' and 'id="id_last_name"'
        )

    def test_edit_page_form_contain_bound_model_instance_data(self):
        """Check, if edit_view is bound existing
        Person model instance data to EditForm"""
        person = Person.objects.first()
        test_response = self.client.get(reverse('hello:edit_page'))
        self.assertIn(
            person.name,
            str(test_response.context['form']['name'])
        )
        self.assertIn(
            person.last_name,
            str(test_response.context['form']['last_name'])
        )

    def test_edit_view_post_request(self):
        """Check, if EditForm post request return proper data"""
        test_response = self.client.post(
            reverse('hello:edit_page'),
            VALID_DATA
        )
        self.assertEqual(test_response.status_code, 200)
        self.assertContains(test_response, "Form submit successfully!")

    def test_edit_view_create_new_Person_istance(self):
        """Check, if EditForm post request create new Person instance,
        if there are no one in DB"""
        Person.objects.all().delete()
        self.assertFalse(Person.objects.first())
        self.client.post(reverse('hello:edit_page'), VALID_DATA)
        self.assertTrue(Person.objects.first())

    def test_edit_view_post_request_update_data_in_DB(self):
        """Check, if EditForm post request update person data in DB"""
        self.client.post(reverse('hello:edit_page'), VALID_DATA)
        person_data = Person.objects.first()
        self.assertEqual(VALID_DATA['name'], person_data.name)
        self.assertEqual(VALID_DATA['last_name'], person_data.last_name)
        self.assertEqual(
            VALID_DATA['date_of_birth'],
            str(person_data.date_of_birth)
        )

    def test_edit_view_post_request_invalid_data_dont_update_data_in_DB(self):
        """Check, if EditForm post request with invalid data,
        don't update person data in DB, but shows errors"""
        test_response = self.client.post(
            reverse('hello:edit_page'),
            INVALID_DATA
        )
        person_data = Person.objects.first()
        self.assertNotEqual(
            INVALID_DATA['name'],
            person_data.name
        )
        self.assertNotEqual(
            INVALID_DATA['last_name'],
            person_data.last_name
        )
        self.assertNotEqual(
            INVALID_DATA['date_of_birth'],
            unicode(person_data.date_of_birth)
        )
        self.assertContains(
            test_response,
            'This field is required.',
            count=2
        )
        self.assertContains(
            test_response,
            'Enter a valid date.'
        )

    def test_edit_view_ajax_post_request_return_proper_data(self):
        """Check, if edit_view ajax post request with valid data,
        return proper JSON response"""
        self.response = self.client.post(
            reverse('hello:edit_page'),
            VALID_DATA,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        ajax_response = json.loads(self.response.content)
        self.assertEqual(ajax_response['status'], 'OK')

    def test_edit_view_ajax_request_no_valid_data_return_errordict(self):
        """Check, if edit_view ajax post request with invalid data,
        return errordict with errors"""
        self.response = self.client.post(
            reverse('hello:edit_page'),
            INVALID_DATA,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        ajax_response = json.loads(self.response.content)
        self.assertEqual(
            ajax_response['name'],
            unicode('* This field is required.')
        )
        self.assertEqual(
            ajax_response['last_name'],
            unicode('* This field is required.')
        )
        self.assertEqual(
            ajax_response['date_of_birth'],
            unicode('* Enter a valid date.')
        )

    def test_edit_page_return_redirect_to_login_page(self):
        """Check, if AnonymousUser request to edit_page,
         return status code 302 and redirect to login_page"""
        test_request = RequestFactory().get(reverse('hello:edit_page'))
        test_request.user = AnonymousUser()
        test_response = edit_view(test_request)
        self.assertEqual(test_response.status_code, 302)
        self.assertIn('login', test_response.url)


class LoginTest(TestCase):

    def test_request_to_login_page_return_correct_status_code(self):
        """Check, if request to login_page return status code 200"""
        test_response = self.client.get('/login/')
        self.assertEqual(test_response.status_code, 200)

    def test_request_to_login_page_uses_proper_template(self):
        """Check, if login_page view render right template"""
        test_response = self.client.get('/login/')
        self.assertTemplateUsed(test_response, 'registration/login.html')
