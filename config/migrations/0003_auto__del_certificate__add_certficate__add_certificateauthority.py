# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Certificate'
        db.delete_table(u'config_certificate')

        # Adding model 'Certficate'
        db.create_table(u'config_certficate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('revoked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('key', self.gf('django.db.models.fields.TextField')()),
            ('certificate', self.gf('django.db.models.fields.TextField')()),
            ('ca', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['config.CertificateAuthority'])),
        ))
        db.send_create_signal(u'config', ['Certficate'])

        # Adding model 'CertificateAuthority'
        db.create_table(u'config_certificateauthority', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('revoked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('key', self.gf('django.db.models.fields.TextField')()),
            ('certificate', self.gf('django.db.models.fields.TextField')()),
            ('next_serial', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'config', ['CertificateAuthority'])


    def backwards(self, orm):
        # Adding model 'Certificate'
        db.create_table(u'config_certificate', (
            ('revoked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('certificate', self.gf('django.db.models.fields.BinaryField')()),
            ('ca', self.gf('django.db.models.fields.related.ForeignKey')(related_name='certificates', null=True, to=orm['config.Certificate'], blank=True)),
            ('key', self.gf('django.db.models.fields.BinaryField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'config', ['Certificate'])

        # Deleting model 'Certficate'
        db.delete_table(u'config_certficate')

        # Deleting model 'CertificateAuthority'
        db.delete_table(u'config_certificateauthority')


    models = {
        u'config.certficate': {
            'Meta': {'object_name': 'Certficate'},
            'ca': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['config.CertificateAuthority']"}),
            'certificate': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.TextField', [], {}),
            'revoked': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'config.certificateauthority': {
            'Meta': {'object_name': 'CertificateAuthority'},
            'certificate': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.TextField', [], {}),
            'next_serial': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'revoked': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['config']