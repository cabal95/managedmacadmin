from django.db import models
from django.utils import timezone
from datetime import datetime


class Machine(models.Model):
    mac = models.CharField(max_length=17, unique=True, db_index=True)
    hostname = models.CharField(max_length=64)
    last_checkin = models.DateTimeField(default=timezone.make_aware(datetime(1, 1, 1, 0, 0), timezone.get_current_timezone()))
    class Meta:
        ordering = ['hostname']


class Fact(models.Model):
    machine = models.ForeignKey(Machine)
    name = models.CharField(max_length=128, db_index=True)
    value = models.TextField(default='')
    last_update = models.DateTimeField(default=timezone.now())
    class Meta:
        ordering = ['name']


class HistoricalFact(models.Model):
    machine = models.ForeignKey(Machine)
    name = models.CharField(max_length=128, db_index=True)
    value = models.TextField(default='')
    timestamp = models.DateTimeField(default=timezone.now(), db_index=True)
    class Meta:
        ordering = ['timestamp', 'name']
