# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management.base import NoArgsCommand
from django.contrib.contenttypes.models import ContentType


class Command(NoArgsCommand):

    def handle(self, **options):
        models = ContentType.objects.filter(app_label='hello')
        for model in models:
            model_cls = model.model_class()
            obj_count = model_cls.objects.count()
            message = model.model + u' : ' + unicode(obj_count)
            self.stdout.write(message)
            error_message = u'error:' + message
            self.stderr.write(error_message)
