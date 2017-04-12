from django.test import TestCase
from apps.hello.forms import EditForm
from django.test import Client


VALID_DATA = {
    'name': 'Alex',
    'last_name': 'Ivanov',
    'date_of_birth': '1945-05-09'
}

INVALID_DATA = {
    'name': 'Alex',
    'last_name': 'Ivanov',
    'date_of_birth': '1945',
    'email': 'vasya.ru',
    'jabber': 'vasya.jb.ru'
}


class TestEditForm(TestCase):

    def setUp(self):
        self.client = Client()

    def test_edit_form_with_no_data(self):
        """Check, if form is invalid, if no data is given"""
        no_data = {}
        form = EditForm(no_data)
        self.assertFalse(form.is_valid())

    def test_edit_form_errors_with_no_data_require(self):
        """Check, form errors, if require data is not given"""
        no_data = {}
        form = EditForm(no_data)
        self.assertEqual(
                        form['name'].errors.as_text(),
                        '* This field is required.'
                            )
        self.assertEqual(
                        form['last_name'].errors.as_text(),
                        '* This field is required.'
                            )
        self.assertEqual(
                        form['date_of_birth'].errors.as_text(),
                        '* This field is required.'
                            )

    def test_edit_form_with_no_correct_person_data(self):
        """Check, if form is  no valid, if invalid person data is given"""
        form = EditForm(INVALID_DATA)
        self.assertFalse(form.is_valid())

    def test_edit_form_errors_with_no_correct_person_data(self):
        """Check, form errors, if given person data is not correct"""
        form = EditForm(INVALID_DATA)
        self.assertEqual(
            form['date_of_birth'].errors.as_text(),
            '* Enter a valid date.'
                                    )
        self.assertEqual(
            form['email'].errors.as_text(),
            '* Enter a valid email address.'
                                    )
        self.assertEqual(
            form['jabber'].errors.as_text(),
            '* Enter a valid email address.'
                                    )

    def test_edit_form_with_correct_person_data(self):
        """Check, if form is valid, if correct person data is given"""
        form = EditForm(VALID_DATA)
        self.assertTrue(form.is_valid())
