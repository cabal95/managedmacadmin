# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'ManagedPreference', fields ['application', 'frequency']
        db.delete_unique(u'mdm_managedpreference', ['application', 'frequency'])

        # Deleting model 'ManagedPreference'
        db.delete_table(u'mdm_managedpreference')

        # Adding model 'DeviceManagedPreference'
        db.create_table(u'mdm_devicemanagedpreference', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mdm.Device'])),
            ('application', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('frequency', self.gf('django.db.models.fields.IntegerField')()),
            ('plist', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'mdm', ['DeviceManagedPreference'])

        # Adding unique constraint on 'DeviceManagedPreference', fields ['device', 'application', 'frequency']
        db.create_unique(u'mdm_devicemanagedpreference', ['device_id', 'application', 'frequency'])


    def backwards(self, orm):
        # Removing unique constraint on 'DeviceManagedPreference', fields ['device', 'application', 'frequency']
        db.delete_unique(u'mdm_devicemanagedpreference', ['device_id', 'application', 'frequency'])

        # Adding model 'ManagedPreference'
        db.create_table(u'mdm_managedpreference', (
            ('plist', self.gf('django.db.models.fields.TextField')()),
            ('application', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('frequency', self.gf('django.db.models.fields.IntegerField')()),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mdm.Device'], null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'mdm', ['ManagedPreference'])

        # Adding unique constraint on 'ManagedPreference', fields ['application', 'frequency']
        db.create_unique(u'mdm_managedpreference', ['application', 'frequency'])

        # Deleting model 'DeviceManagedPreference'
        db.delete_table(u'mdm_devicemanagedpreference')


    models = {
        u'mdm.command': {
            'Meta': {'object_name': 'Command'},
            'data': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'date_requested': ('django.db.models.fields.DateTimeField', [], {}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mdm.Device']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'db_index': 'True'})
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
            'locator_service': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'os_version': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '16', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'product_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'push_magic': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'push_token': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'push_topic': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'supervised': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'udid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'db_index': 'True'}),
            'wifi_mac': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '17', 'blank': 'True'})
        },
        u'mdm.devicemanagedpreference': {
            'Meta': {'unique_together': "(('device', 'application', 'frequency'),)", 'object_name': 'DeviceManagedPreference'},
            'application': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mdm.Device']"}),
            'frequency': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plist': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['mdm']