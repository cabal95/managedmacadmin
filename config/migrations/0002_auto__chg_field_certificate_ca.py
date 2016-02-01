# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Certificate.ca'
        db.alter_column(u'config_certificate', 'ca_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['config.Certificate']))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Certificate.ca'
        raise RuntimeError("Cannot reverse this migration. 'Certificate.ca' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Certificate.ca'
        db.alter_column(u'config_certificate', 'ca_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['config.Certificate']))

    models = {
        u'config.certificate': {
            'Meta': {'object_name': 'Certificate'},
            'ca': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'certificates'", 'null': 'True', 'to': u"orm['config.Certificate']"}),
            'certificate': ('django.db.models.fields.BinaryField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.BinaryField', [], {}),
            'revoked': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['config']