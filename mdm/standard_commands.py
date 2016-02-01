from django.conf import settings
from models import Device, AppInventoryItem, DeviceProfile, ProfileInventoryItem
import commands
import plistlib


def device_information_data(command):
    return {
	'RequestType': 'DeviceInformation',
	'Queries': [
		'DeviceName',
		'OSVersion',
		'BuildVersion',
		'ModelName',
		'Model',
		'ProductName',
		'SerialNumber',
		'DeviceCapacity',
		'AvailableDeviceCapacity',
		'BatteryLevel',
		'IsSupervised',
		'IsDeviceLocatorServiceEnabled',
		'IsActivationLockEnabled',
		'IsCloudBackupEnabled',
		'BluetoothMAC',
		'WiFiMAC',
		'EthernetMAC',
		'PhoneNumber',
		'DeviceID',
	]
    }

def device_information_response(command, response):
    responses = response['QueryResponses']

    if 'DeviceName' in responses:
        command.device.name = responses['DeviceName']

    if 'OSVersion' in responses:
        command.device.os_version = responses['OSVersion']

    if 'BuildVersion' in responses:
        command.device.build_version = responses['BuildVersion']

    if 'Model' in responses:
        command.device.model = responses['Model']

    if 'ModelName' in responses:
        command.device.model_name = responses['ModelName']

    if 'ProductName' in responses:
        command.device.product_name = responses['ProductName']
        if command.device.product_name[:4] == 'iPod':
            command.device.type = Device.IPOD
        elif command.device.product_name[:6] == 'iPhone':
            command.device.type = Device.IPHONE
        elif command.device.product_name[:4] == 'iPad':
            command.device.type = Device.IPAD
        elif command.device.product_name[:7] == 'AppleTV':
            command.device.type = Device.APPLETV
        elif command.device.product_name[:4] == 'iMac':
            command.device.type = Device.DESKTOP
        elif command.device.product_name[:7] == 'Macmini':
            command.device.type = Device.DESKTOP
        elif command.device.product_name[:6] == 'MacPro':
            command.device.type = Device.DESKTOP
        elif command.device.product_name[:10] == 'MacBookPro':
            command.device.type = Device.LAPTOP
        elif command.device.product_name[:10] == 'MacBookAir':
            command.device.type = Device.LAPTOP
        elif command.device.product_name[:7] == 'MacBook':
            command.device.type = Device.LAPTOP
        else:
            command.device.type = Device.OTHER

        if command.device.type == Device.IPOD or command.device.type == Device.IPHONE or command.device.type == Device.IPAD or command.device.type == Device.APPLETV:
            command.device.os = Device.IOS
        elif command.device.type == Device.LAPTOP or command.device.type == Device.DESKTOP:
            command.device.os = Device.OSX
        else:
            command.device.os = Device.OTHER

    if 'SerialNumber' in responses:
        command.device.serial_number = responses['SerialNumber']

    if 'DeviceCapacity' in responses:
        command.device.capacity = responses['DeviceCapacity']

    if 'AvailableDeviceCapacity' in responses:
        command.device.available_capacity = responses['AvailableDeviceCapacity']

    if 'BatteryLevel' in responses:
        command.device.battery_level = responses['BatteryLevel']

    if 'IsSupervised' in responses:
        command.device.supervised = responses['IsSupervised']

    if 'IsDeviceLocatorServiceEnabled' in responses:
        command.device.locator_service = responses['IsDeviceLocatorServiceEnabled']

    if 'IsActivationLockEnabled' in responses:
        command.device.activation_lock = responses['IsActivationLockEnabled']

    if 'IsCloudBackupEnabled' in responses:
        command.device.cloud_backup = responses['IsCloudBackupEnabled']

    if 'BluetoothMAC' in responses:
        command.device.bluetooth_mac = responses['BluetoothMAC'].replace("-", ":")

    if 'WiFiMAC' in responses:
        command.device.wifi_mac = responses['WiFiMAC']

    if 'EthernetMAC' in responses:
        command.device.ethernet_mac = responses['EthernetMAC']

    if 'PhoneNumber' in responses:
        command.device.phone_number = responses['PhoneNumber']

    if 'DeviceID' in responses:
        # Apple TV uses DeviceID for EthernetMAC
        command.device.ethernet_mac = responses['DeviceID']

    command.device.save()

    return True


def installed_applications_data(command):
    return {
	'RequestType': 'InstalledApplicationList'
    }

def installed_applications_response(command, response):
    if 'InstalledApplicationList' not in response:
        return False

    # Remove all the old apps for this device.
    AppInventoryItem.objects.filter(device=command.device).delete()

    for item in response['InstalledApplicationList']:
        if 'Name' not in item or 'Identifier' not in item or 'Version' not in item:
            continue

        app = AppInventoryItem(device=command.device)
        if len(item['Name']) > 0:
            app.name = item['Name']
        else:
            app.name = item['Identifier']
        app.identifier = item['Identifier']
        app.version = item['Version']
        if 'BundleSize' in item:
            app.bundle_size = item['BundleSize']
        if 'ShortVersion' in item:
            app.short_version = item['ShortVersion']
        else:
            app.short_version = item['Version']
        if 'DynamicSize' in item:
            app.dynamic_size = item['DynamicSize']
        app.save()

    return True


def installed_profiles_data(command):
    return {
	'RequestType': 'ProfileList'
    }

def installed_profiles_response(command, response):
    if 'ProfileList' not in response:
        return False

    # Remove all the old profiles for this device.
    ProfileInventoryItem.objects.filter(device=command.device).delete()

    for item in response['ProfileList']:
        profile = ProfileInventoryItem(device=command.device)
        if len(item['PayloadDisplayName']) > 0:
            profile.name = item['PayloadDisplayName']
        else:
            profile.name = item['PayloadIdentifier']
        if 'PayloadDescription' in item:
            profile.description = item['PayloadDescription']
        profile.identifier = item['PayloadIdentifier']
        profile.uuid = item['PayloadUUID']

        profile.save()

    return True


def install_profile_data(command):
    profile = DeviceProfile.objects.get(device=command.device, identifier=command.data)
    data = dict()
    data['RequestType'] = 'InstallProfile'
    data['Payload'] = plistlib.Data(profile.payload)

    return data


def install_profile_response(command, response):
    return True


def initialize():
    commands.registerCommandHandler(
	'com.github.managedmacadmin.DeviceInformation',
	device_information_data,
	device_information_response)

    commands.registerCommandHandler(
	'com.github.managedmacadmin.ProfileList',
	installed_profiles_data,
	installed_profiles_response)

    commands.registerCommandHandler(
	'com.github.managedmacadmin.InstalledApplicationList',
	installed_applications_data,
	installed_applications_response)

    commands.registerCommandHandler(
        'com.github.managedmacadmin.InstallProfile',
        install_profile_data,
        install_profile_response)
