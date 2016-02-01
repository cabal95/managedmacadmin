# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Device'
        db.create_table(u'mdm_device', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('udid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=36, db_index=True)),
            ('push_topic', self.gf('django.db.models.fields.CharField')(max_length=96)),
            ('push_token', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('push_magic', self.gf('django.db.models.fields.CharField')(max_length=48)),
            ('last_checkin', self.gf('django.db.models.fields.DateTimeField')()),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
            ('os_version', self.gf('django.db.models.fields.CharField')(default='', max_length=16)),
            ('build_version', self.gf('django.db.models.fields.CharField')(default='', max_length=16)),
            ('model', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
            ('product_name', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
            ('serial_number', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=32)),
            ('capacity', self.gf('django.db.models.fields.FloatField')(default=None, null=True, blank=True)),
            ('available_capacity', self.gf('django.db.models.fields.FloatField')(default=None, null=True, blank=True)),
            ('battery_level', self.gf('django.db.models.fields.FloatField')(default=None, null=True, blank=True)),
            ('supervised', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
            ('locator_service', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
            ('activation_lock', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
            ('cloud_backup', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
            ('bluetooth_mac', self.gf('django.db.models.fields.CharField')(default='', max_length=17)),
            ('wifi_mac', self.gf('django.db.models.fields.CharField')(default='', max_length=17)),
            ('ethernet_mac', self.gf('django.db.models.fields.CharField')(default='', max_length=288)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
        ))
        db.send_create_signal(u'mdm', ['Device'])

        # Adding model 'Command'
        db.create_table(u'mdm_command', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mdm.Device'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('date_requested', self.gf('django.db.models.fields.DateTimeField')()),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, db_index=True)),
            ('command', self.gf('django.db.models.fields.CharField')(max_length=8000)),
        ))
        db.send_create_signal(u'mdm', ['Command'])

        # Adding model 'ManagedPreference'
        db.create_table(u'mdm_managedpreference', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mdm.Device'], null=True, blank=True)),
            ('application', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('frequency', self.gf('django.db.models.fields.IntegerField')()),
            ('plist', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'mdm', ['ManagedPreference'])

        # Adding unique constraint on 'ManagedPreference', fields ['application', 'frequency']
        db.create_unique(u'mdm_managedpreference', ['application', 'frequency'])


    def backwards(self, orm):
        # Removing unique constraint on 'ManagedPreference', fields ['application', 'frequency']
        db.delete_unique(u'mdm_managedpreference', ['application', 'frequency'])

        # Deleting model 'Device'
        db.delete_table(u'mdm_device')

        # Deleting model 'Command'
        db.delete_table(u'mdm_command')

        # Deleting model 'ManagedPreference'
        db.delete_table(u'mdm_managedpreference')


    models = {
        u'mdm.command': {
            'Meta': {'object_name': 'Command'},
            'command': ('django.db.models.fields.CharField', [], {'max_length': '8000'}),
            'date_requested': ('django.db.models.fields.DateTimeField', [], {}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mdm.Device']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'db_index': 'True'})
        },
        u'mdm.device': {
            'Meta': {'object_name': 'Device'},
            'activation_lock': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'available_capacity': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'battery_level': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'bluetooth_mac': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '17'}),
            'build_version': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '16'}),
            'capacity': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'cloud_backup': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'ethernet_mac': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '288'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_checkin': ('django.db.models.fields.DateTimeField', [], {}),
            'locator_service': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'os_version': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '16'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'product_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'push_magic': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'push_token': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'push_topic': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'serial_number': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '32'}),
            'supervised': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'udid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'db_index': 'True'}),
            'wifi_mac': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '17'})
        },
        u'mdm.managedpreference': {
            'Meta': {'unique_together': "(('application', 'frequency'),)", 'object_name': 'ManagedPreference'},
            'application': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mdm.Device']", 'null': 'True', 'blank': 'True'}),
            'frequency': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plist': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['mdm']