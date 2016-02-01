from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from datetime import datetime, timedelta
from mdm.models import DeviceCommand, Device, DeviceCheckin
import mdm.push
import uuid


class Command(BaseCommand):
    help = 'Run automated tasks'

    def handle(self, *args, **options):
        self.CheckTypeNeeded(6, "com.github.managedmacadmin.DeviceInformation", UpdateDeviceInformation)
        self.CheckTypeNeeded(24, "com.github.managedmacadmin.ProfileList", UpdateProfileList)
        self.CheckTypeNeeded(24, "com.github.managedmacadmin.InstalledApplicationList", UpdateInstalledApplicationList)

        since = datetime.now() - timedelta(minutes=30)
        devices = Device.objects.filter(last_checkin__lt=since, last_notification__lt=since)
        RequestDeviceCheckin(devices)


    def CheckTypeNeeded(self, hours, type, handler):
        age = datetime.now() - timedelta(hours=hours)
        devices = Device.objects.all()
        recent = DeviceCommand.objects.filter(type=type, status=DeviceCommand.SUCCESS, date_completed__gte=age).values('device').distinct()
        failed = DeviceCommand.objects.filter(type=type, status=DeviceCommand.FAILED, date_completed__gte=age).values('device').distinct()
        pending = DeviceCommand.objects.filter(type=type, status=DeviceCommand.PENDING).values('device').distinct()
        devices = Device.objects.exclude(pk__in=recent).exclude(pk__in=pending).exclude(pk__in=failed)
        if devices.count() > 0:
            handler(type, devices)


def UpdateDeviceInformation(type, devices):
    for device in devices:
        DeviceCommand.NewDeviceInformation(device)
        mdm.push.push_notification(device)


def UpdateProfileList(type, devices):
    for device in devices:
        DeviceCommand.NewProfileList(device)
        mdm.push.push_notification(device)


def UpdateInstalledApplicationList(type, devices):
    for device in devices:
        DeviceCommand.NewInstalledApplicationList(device)
        mdm.push.push_notification(device)


def RequestDeviceCheckin(devices):
    for device in devices:
        mdm.push.push_notification(device)
