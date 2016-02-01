# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'DeviceCheckin.date'
        db.delete_column(u'mdm_devicecheckin', 'date')

        # Adding field 'DeviceCheckin.start_date'
        db.add_column(u'mdm_devicecheckin', 'start_date',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 9, 0, 0)),
                      keep_default=False)

        # Adding field 'DeviceCheckin.end_date'
        db.add_column(u'mdm_devicecheckin', 'end_date',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 9, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'DeviceCheckin.date'
        raise RuntimeError("Cannot reverse this migration. 'DeviceCheckin.date' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'DeviceCheckin.date'
        db.add_column(u'mdm_devicecheckin', 'date',
                      self.gf('django.db.models.fields.DateTimeField')(),
                      keep_default=False)

        # Deleting field 'DeviceCheckin.start_date'
        db.delete_column(u'mdm_devicecheckin', 'start_date')

        # Deleting field 'DeviceCheckin.end_date'
        db.delete_column(u'mdm_devicecheckin', 'end_date')


    models = {
        u'mdm.appinventoryitem': {
            'Meta': {'ordering': "['name', '-version']", 'object_name': 'AppInventoryItem'},
            'bundle_size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mdm.Device']"}),
            'dynamic_size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'short_version': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '32'})
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
        u'mdm.devicecheckin': {
            'Meta': {'object_name': 'DeviceCheckin'},
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '48'}),
            'country_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '8'}),
            'country_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mdm.Device']"}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'region_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '16'}),
            'region_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'mdm.devicecommand': {
            'Meta': {'object_name': 'DeviceCommand'},
            'attempts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'data': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'date_completed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_requested': ('django.db.models.fields.DateTimeField', [], {}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mdm.Device']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'db_index': 'True'})
        },
        u'mdm.devicemanagedpreference': {
            'Meta': {'unique_together': "(('device', 'application', 'frequency'),)", 'object_name': 'DeviceManagedPreference'},
            'application': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mdm.Device']"}),
            'frequency': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plist': ('django.db.models.fields.TextField', [], {})
        },
        u'mdm.deviceprofile': {
            'Meta': {'unique_together': "(('device', 'identifier'),)", 'object_name': 'DeviceProfile'},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mdm.Device']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'payload': ('django.db.models.fields.TextField', [], {}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36'})
        },
        u'mdm.lastcommandstatus': {
            'Meta': {'object_name': 'LastCommandStatus'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mdm.Device']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'mdm.profileinventoryitem': {
            'Meta': {'object_name': 'ProfileInventoryItem'},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mdm.Device']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'})
        }
    }

    complete_apps = ['mdm']