# -*- coding: utf-8 -*-
from django.test import TestCase
from apps.hello.models import Person
from django.test.utils import override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.conf import settings
import shutil


@override_settings(MEDIA_ROOT=settings.MEDIA_TEST_ROOT)
class PersonModelTest(TestCase):

    def setUp(self):
        self.test_person = Person.objects.first()
        self.test_img_path = os.path.join(
            settings.BASE_DIR,
            'assets/img/test_image.png'
        )
        with open(self.test_img_path, 'rb') as test_img:
            self.test_image_1 = SimpleUploadedFile(
                name='test_image_1.png',
                content=test_img.read(),
                content_type='image/png'
            )
        self.test_person.photo = self.test_image_1
        self.test_person.save()
        self.first_photo_file = self.test_person.photo.path

    def tearDown(self):
        test_dir = os.path.exists(settings.MEDIA_TEST_ROOT)
        if test_dir:
            shutil.rmtree(settings.MEDIA_TEST_ROOT)

    def test_save_method(self):
        """Check, if model save method,
         save first person photo to proper filesystem path,
         and crop image to proper size"""
        self.assertTrue(os.path.exists(self.first_photo_file))
        self.assertEqual(
            self.first_photo_file,
            settings.MEDIA_TEST_ROOT + self.test_person.photo.name
        )
        self.assertTrue(
            self.test_person.photo.width <= 200 and
            self.test_person.photo.height <= 200
        )

    def test_save_method_remove_unused_img(self):
        """Check, if model save method delete unused images"""
        with open(self.test_img_path, 'rb') as test_img:
            self.test_image_2 = SimpleUploadedFile(
                name='test_image_2.png',
                content=test_img.read(),
                content_type='image/png'
            )
        self.test_person.photo = self.test_image_2
        self.test_person.save()
        self.second_photo_file = self.test_person.photo.path
        self.assertTrue(os.path.exists(self.second_photo_file))
        self.assertFalse(os.path.exists(self.first_photo_file))
