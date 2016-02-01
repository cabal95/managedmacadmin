# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Certificate.serial'
        db.add_column(u'config_certificate', 'serial',
                      self.gf('django.db.models.fields.IntegerField')(default=-1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Certificate.serial'
        db.delete_column(u'config_certificate', 'serial')


    models = {
        u'config.certificate': {
            'Meta': {'object_name': 'Certificate'},
            'ca': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['config.CertificateAuthority']"}),
            'crt': ('django.db.models.fields.TextField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mdm.Device']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.TextField', [], {}),
            'md5': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'revoked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'serial': ('django.db.models.fields.IntegerField', [], {})
        },
        u'config.certificateauthority': {
            'Meta': {'object_name': 'CertificateAuthority'},
            'crt': ('django.db.models.fields.TextField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.TextField', [], {}),
            'next_serial': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'revoked': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'mdm.device': {
            'Meta': {'object_name': 'Device'},
            'activation_lock': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'available_capacity': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'battery_level': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'bluetooth_mac': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '17', 'blank': 'True'}),
            'build_version': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '16', 'blank': 'True'}),
            'capacity': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'cloud_backup': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'ethernet_mac': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '288', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_checkin': ('django.db.models.fields.DateTimeField', [], {}),
            'last_notification': ('django.db.models.fields.DateTimeField', [], {}),
            'locator_service': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'os': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'os_version': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '16', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'product_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'push_magic': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'push_token': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'push_topic': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'supervised': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'udid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'db_index': 'True'}),
            'wifi_mac': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '17', 'blank': 'True'})
        }
    }

    complete_apps = ['config']