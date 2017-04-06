# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.core.management import call_command


class Migration(DataMigration):

    def forwards(self, orm):
        call_command("loaddata", "requests_data.json")

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'hello.requestslog': {
            'Meta': {'ordering': "[u'-request_time']", 'object_name': 'RequestsLog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'request_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status_code': ('django.db.models.fields.IntegerField', [], {'max_length': '3'})
        }
    }

    complete_apps = ['hello']
    symmetrical = True

