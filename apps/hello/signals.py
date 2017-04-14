# -*- coding: utf-8 -*-
from apps.hello.models import ModelsLog, Person, RequestsLog
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


LOG_MODELS = [Person, RequestsLog]


@receiver(post_save)
def model_save_handler(sender, created, **kwargs):
    if sender in LOG_MODELS:
        if created:
            action = 'ADD'
            rep_act = 'created'
        else:
            action = 'EDIT'
            rep_act = 'edited'
        model_log = ModelsLog(
            content_object=kwargs['instance'],
            action=action,
            report='%s(%s object id=%s) has %s' % (
                kwargs['instance'],
                sender.__name__,
                kwargs['instance'].id,
                rep_act
            )
        )
        model_log.save()


@receiver(post_delete)
def model_del_handler(sender, **kwargs):
    if sender in LOG_MODELS:
        model_log = ModelsLog(
            content_object=kwargs['instance'],
            action='DEL',
            report='%s(%s object id=%s) has %s' % (
                kwargs['instance'],
                sender.__name__,
                kwargs['instance'].id,
                'deleted'
            )
        )
        model_log.save()
