# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Certificate'
        db.create_table(u'config_certificate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('revoked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('key', self.gf('django.db.models.fields.BinaryField')()),
            ('certificate', self.gf('django.db.models.fields.BinaryField')()),
            ('ca', self.gf('django.db.models.fields.related.ForeignKey')(related_name='certificates', to=orm['config.Certificate'])),
        ))
        db.send_create_signal(u'config', ['Certificate'])


    def backwards(self, orm):
        # Deleting model 'Certificate'
        db.delete_table(u'config_certificate')


    models = {
        u'config.certificate': {
            'Meta': {'object_name': 'Certificate'},
            'ca': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'certificates'", 'to': u"orm['config.Certificate']"}),
            'certificate': ('django.db.models.fields.BinaryField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.BinaryField', [], {}),
            'revoked': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['config']