# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Certficate'
        db.delete_table(u'config_certficate')

        # Adding model 'Certificate'
        db.create_table(u'config_certificate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('revoked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('key', self.gf('django.db.models.fields.TextField')()),
            ('crt', self.gf('django.db.models.fields.TextField')()),
            ('ca', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['config.CertificateAuthority'])),
        ))
        db.send_create_signal(u'config', ['Certificate'])

        # Deleting field 'CertificateAuthority.certificate'
        db.delete_column(u'config_certificateauthority', 'certificate')

        # Adding field 'CertificateAuthority.crt'
        db.add_column(u'config_certificateauthority', 'crt',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Certficate'
        db.create_table(u'config_certficate', (
            ('revoked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('certificate', self.gf('django.db.models.fields.TextField')()),
            ('ca', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['config.CertificateAuthority'])),
            ('key', self.gf('django.db.models.fields.TextField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'config', ['Certficate'])

        # Deleting model 'Certificate'
        db.delete_table(u'config_certificate')


        # User chose to not deal with backwards NULL issues for 'CertificateAuthority.certificate'
        raise RuntimeError("Cannot reverse this migration. 'CertificateAuthority.certificate' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'CertificateAuthority.certificate'
        db.add_column(u'config_certificateauthority', 'certificate',
                      self.gf('django.db.models.fields.TextField')(),
                      keep_default=False)

        # Deleting field 'CertificateAuthority.crt'
        db.delete_column(u'config_certificateauthority', 'crt')


    models = {
        u'config.certificate': {
            'Meta': {'object_name': 'Certificate'},
            'ca': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['config.CertificateAuthority']"}),
            'crt': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.TextField', [], {}),
            'revoked': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'config.certificateauthority': {
            'Meta': {'object_name': 'CertificateAuthority'},
            'crt': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.TextField', [], {}),
            'next_serial': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'revoked': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['config']