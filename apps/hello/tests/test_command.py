# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO
from django.contrib.contenttypes.models import ContentType


class ModelsCountCommandTest(TestCase):

    def test_models_count_command_std_out(self):
        """Check, if models_count command prints proper data in stdOut"""
        models_list = (
            ContentType
            .objects
            .filter(app_label='hello')
        )
        std_out = StringIO()
        call_command('models_count', stdout=std_out)
        std_out_content = std_out.getvalue()
        for model in models_list:
            model_cls = model.model_class()
            model_name = model.model
            obj_count = model_cls.objects.count()
            self.assertIn(
                '%s : %d' % (model_name, obj_count),
                std_out_content
            )

    def test_models_count_command_std_err(self):
        """Check, if models_count command prints proper data in stdErr"""
        models_list = (
            ContentType
            .objects
            .filter(app_label='hello')
        )
        std_err = StringIO()
        call_command('models_count', stderr=std_err)
        std_err_content = std_err.getvalue()
        for model in models_list:
            model_cls = model.model_class()
            model_name = model.model
            obj_count = model_cls.objects.count()
            self.assertIn(
                'error:%s : %d' % (model_name, obj_count),
                std_err_content
            )
