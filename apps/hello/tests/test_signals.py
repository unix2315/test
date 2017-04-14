# -*- coding: utf-8 -*-
from django.test import TestCase
from apps.hello.models import Person
from datetime import date


PERSON_DATA = {
    'name': 'Alex',
    'last_name': 'Ivanov',
    'date_of_birth': date(1945, 5, 9)
}


class SignalsTest(TestCase):

    def setUp(self):
        self.test_person = Person(**PERSON_DATA)
        self.test_person.save()

    def test_save_signal_handler(self):
        """Check, if a creation a new object, is add
        a new 'ADD' entry in ModelsLog model"""
        last_log = ModelsLog.objects.last()
        self.assertEqual(last_log.action, 'ADD')
        self.assertIn(self.test_person, last_log.report)

    def test_update_signal_handler(self):
        """Check, if a update an object, is add
        a new 'EDIT' entry in ModelsLog model"""
        self.test_person.name = 'Vasily'
        self.test_person.last_name = 'Zaycev'
        self.test_person.save()
        last_log = ModelsLog.objects.last()
        self.assertEqual(last_log.action, 'EDIT')
        self.assertIn(self.test_person, last_log.report)

    def test_delete_signal_hendler(self):
        """Check, if a delete an object, is add
        a new 'DEL' entry in ModelsLog model"""
        self.test_person.delete()
        last_log = ModelsLog.objects.last()
        self.assertTrue(last_log)
        self.assertEqual(last_log.action, 'DEL')
        self.assertIn('Alex Ivanov' and 'has deleted', last_log.report)
