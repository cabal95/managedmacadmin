from django.db import models
from datetime import datetime
import calendar
import base64
import plistlib
import uuid


class Device(models.Model):
    UNKNOWN = 0
    IPOD = 1
    IPHONE = 2
    IPAD = 3
    APPLETV = 4
    DESKTOP = 5
    LAPTOP = 6
    OTHER = 99
    TYPE_CHOICES = (
        (UNKNOWN, 'Unknown'),
        (IPOD, 'iPod'),
        (IPHONE, 'iPhone'),
        (IPAD, 'iPad'),
        (APPLETV, 'AppleTV'),
        (DESKTOP, 'Desktop'),
        (LAPTOP, 'Laptop'),
        (OTHER, 'Other'),
    )
    IOS = 1
    OSX = 2
    OS_CHOICES = (
        (UNKNOWN, 'Unknown'),
        (IOS, 'iOS'),
        (OSX, 'Mac OS X'),
        (OTHER, 'Other'),
    )

    udid = models.CharField(max_length=36, unique=True, db_index=True)
    push_topic = models.CharField(max_length=96)
    push_token = models.CharField(max_length=256)
    push_magic = models.CharField(max_length=48)
    last_checkin = models.DateTimeField()
    last_notification = models.DateTimeField()
    name = models.CharField(max_length=128, blank=True, default="")
    type = models.IntegerField(choices=TYPE_CHOICES, default=UNKNOWN)
    os = models.IntegerField(choices=OS_CHOICES, default=UNKNOWN)
    os_version = models.CharField(max_length=16, blank=True, default="")
    build_version = models.CharField(max_length=16, blank=True, default="")
    model = models.CharField(max_length=32, blank=True, default="")
    model_name = models.CharField(max_length=32, blank=True, default="")
    product_name = models.CharField(max_length=32, blank=True, default="")
    serial_number = models.CharField(max_length=32, blank=True)
    capacity = models.FloatField(default=None, null=True, blank=True)
    available_capacity = models.FloatField(default=None, null=True, blank=True)
    battery_level = models.FloatField(default=None, null=True, blank=True)
    supervised = models.NullBooleanField(default=None)
    locator_service = models.NullBooleanField(default=None)
    activation_lock = models.NullBooleanField(default=None)
    cloud_backup = models.NullBooleanField(default=None)
    bluetooth_mac = models.CharField(max_length=17, blank=True, default="")
    wifi_mac = models.CharField(max_length=17, blank=True, default="")
    ethernet_mac = models.CharField(max_length=288, blank=True, default="")
    phone_number = models.CharField(max_length=32, blank=True, default="")

    def __str__(self):
        if self.name:
            return self.name
        return self.udid

    def all_groups(self):
        groups = []
        items = self.devicegroup_set.order_by('-priority').all()
        for group in items:
            if group not in groups:
                groups.append(group)
            for g in group.recursive_groups():
                if g not in groups:
                    groups.append(g)
        return groups


class DeviceCheckin(models.Model):
    device = models.ForeignKey(Device)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    ip = models.CharField(max_length=64, default="")
    latitude = models.FloatField(default=0, null=True, blank=True)
    longitude = models.FloatField(default=0, null=True, blank=True)
    country_code = models.CharField(max_length=8, default="")
    region_code = models.CharField(max_length=16, default="")
    city = models.CharField(max_length=48, default="")
    country_name = models.CharField(max_length=64, default="")
    region_name = models.CharField(max_length=64, default="")


class DeviceCommand(models.Model):
    PENDING = 1
    RUNNING = 2
    SUCCESS = 3
    FAILED = 4
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (RUNNING, 'Running'),
        (SUCCESS, 'Success'),
        (FAILED, 'Failed'),
    )
    device = models.ForeignKey(Device)
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    data = models.CharField(max_length=256, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
    attempts = models.IntegerField(default=0)
    date_requested = models.DateTimeField()
    date_completed = models.DateTimeField(blank=True, null=True)
    uuid = models.CharField(max_length=36, db_index=True)

    def __str__(self):
        return self.name

    @classmethod
    def NewCommand(cls, device, name, type, data):
        if data == None:
            data = ''
        cmd = DeviceCommand.objects.filter(device=device, type=type, data=data, status=DeviceCommand.PENDING).first()
        if cmd != None:
            return None

        cmd = DeviceCommand(device=device)
        cmd.name = name
        cmd.type = type
        cmd.data = data
        cmd.status = DeviceCommand.PENDING
        cmd.date_requested = datetime.now()
        cmd.uuid = str(uuid.uuid4())
        cmd.save()

        return cmd

    @classmethod
    def InstallProfile(cls, device, profile):
        cls.NewCommand(device, 'Install Profile: ' + profile.name,
            'com.github.managedmacadmin.InstallProfile', profile.identifier)

    @classmethod
    def NewDeviceInformation(cls, device):
        return cls.NewCommand(device, 'Query Device Information',
            'com.github.managedmacadmin.DeviceInformation', None)
        
    @classmethod
    def NewProfileList(cls, device):
        return cls.NewCommand(device, 'Query Installed Profiles',
            'com.github.managedmacadmin.ProfileList', None)
        
    @classmethod
    def NewInstalledApplicationList(cls, device):
        return cls.NewCommand(device, 'Query Installed Applications',
            'com.github.managedmacadmin.InstalledApplicationList', None)
        


class DeviceProfile(models.Model):
    device = models.ForeignKey(Device)
    name = models.CharField(max_length=128)
    identifier = models.CharField(max_length=128)
    uuid = models.CharField(max_length=36)
    payload = models.TextField()
    class Meta:
        unique_together = (("device", "identifier"),)


class DeviceManagedPreference(models.Model):
    # Set-Once with mcx_data_timestamp = Sets once, never again. (MCX Once)
    # Set-Once without mcx_data_timestamp = Sets at each login. (MCX Often)
    # Date in the timestamp doesn't seem to make a difference.
    #
    # Other keys to lookup, mcx_union_policy_keys
    #
    device = models.ForeignKey(Device)
    identifier = models.CharField(max_length=200)
    plist = models.TextField()
    class Meta:
        unique_together = (("device", "identifier"),)


class DeviceGroup(models.Model):
    name = models.CharField(max_length=128, unique=True)
    uuid = models.CharField(max_length=36)
    description = models.TextField(blank=True)
    priority = models.IntegerField(default=0)
    devices = models.ManyToManyField(Device)
    groups = models.ManyToManyField("DeviceGroup")

    def __str__(self):
        return self.name

    # Retrieve a recursive list of all groups contained by this group.
    def recursive_groups(self):
        groups = []
        items = self.groups.order_by('-priority').all()
        for group in items:
            if group not in groups:
                groups.append(group)
            for g in group.recursive_groups():
                if g not in groups:
                    groups.append(g)
        return groups

    # Retrieve a recursive list of all parent groups that contain this group.
    def recursive_parents(self):
        groups = []
        items = self.devicegroup_set.order_by('priority').all()
        for group in items:
            if group not in groups:
                groups.append(group)
            for g in group.recursive_parents():
                if g not in groups:
                    groups.append(g)
        return groups

    # Retrieve a list of all devices in this group or in groups that contain this group.
    def recursive_devices(self):
        groups = self.recursive_parents()
        devices = []
        for d in self.devices.all():
            devices.append(d)
        for group in groups:
            for d in group.devices.all():
                if d not in devices:
                    devices.append(d)
        return devices

class DeviceGroupManagedPreference(models.Model):
    # Set-Once with mcx_data_timestamp = Sets once, never again. (MCX Once)
    # Set-Once without mcx_data_timestamp = Sets at each login. (MCX Often)
    # Date in the timestamp doesn't seem to make a difference.
    #
    # Other keys to lookup, mcx_union_policy_keys
    #
    group = models.ForeignKey(DeviceGroup)
    identifier = models.CharField(max_length=200)
    plist = models.TextField()
    class Meta:
        unique_together = (("group", "identifier"),)


class AppInventoryItem(models.Model):
    device = models.ForeignKey(Device)
    name = models.CharField(max_length=256)
    identifier = models.CharField(max_length=256)
    version = models.CharField(max_length=32)
    short_version = models.CharField(max_length=32)
    bundle_size = models.IntegerField(default=0)
    dynamic_size = models.IntegerField(default=0)
    class Meta:
        ordering = ['name', '-version']


class ProfileInventoryItem(models.Model):
    device = models.ForeignKey(Device)
    name = models.CharField(max_length=256, default='')
    description = models.CharField(max_length=1024, default='')
    identifier = models.CharField(max_length=256, default='')
    uuid = models.CharField(max_length=128, default='')
