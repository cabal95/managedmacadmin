from django.contrib import admin
from mdm.models import Device, DeviceCommand, AppInventoryItem, DeviceCheckin, DeviceProfile, DeviceManagedPreference, ProfileInventoryItem, DeviceGroup, DeviceGroupManagedPreference

admin.site.register(Device)
admin.site.register(DeviceCommand)
admin.site.register(AppInventoryItem)
admin.site.register(ProfileInventoryItem)
admin.site.register(DeviceCheckin)
admin.site.register(DeviceProfile)
admin.site.register(DeviceManagedPreference)
admin.site.register(DeviceGroup)
admin.site.register(DeviceGroupManagedPreference)
