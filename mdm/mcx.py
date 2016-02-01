from django.conf import settings
from models import DeviceProfile, DeviceManagedPreference, DeviceGroupManagedPreference, Device, DeviceGroup, DeviceCommand
from datetime import datetime
import uuid
import plistlib
import push


def build_system_configuration_profile(device, install = False):
    # Configuration Profiles are only valid on OS X.
    if device.os != Device.OSX:
        return

    plist = { }
    plist['PayloadDisplayName'] = 'System Device Configuration'
    plist['PayloadDescription'] = 'Managed Preferences for Device'
    plist['PayloadIdentifier'] = settings.MANAGED_PROFILE_IDENTIFIER + '.ManagedPreferences'
    plist['PayloadOrganization'] = settings.ORGANIZATION
    plist['PayloadRemovalDisallowed'] = False
    plist['PayloadVersion'] = 1
    plist['PayloadType'] = 'Configuration'
    plist['PayloadScope'] = 'System'
    plist['PayloadUUID'] = str(uuid.uuid4())

    plist['PayloadContent'] = [ ]
    apps = build_custom_preference_profile(device)
    for app in apps:
        payload = { }
        payload['PayloadEnabled'] = True
        payload['PayloadType'] = 'com.apple.ManagedClient.preferences'
        payload['PayloadUUID'] = str(uuid.uuid4())
        payload['PayloadIdentifier'] = plist['PayloadIdentifier'] + '.alacarte.customsettings.' + payload['PayloadUUID']
        payload['PayloadVerison'] = 1
        payload['PayloadContent'] = { app: apps[app] }
        plist['PayloadContent'].append(payload)

    if DeviceProfile.objects.filter(device=device, identifier=plist['PayloadIdentifier']).count() == 0:
        profile = DeviceProfile(device=device)
    else:
        profile = DeviceProfile.objects.get(device=device, identifier=plist['PayloadIdentifier'])
    profile.name = plist['PayloadDisplayName']
    profile.identifier = plist['PayloadIdentifier']
    profile.uuid = plist['PayloadUUID']

    profile.payload = plistlib.writePlistToString(plist)

    profile.save()

    if install == True:
        DeviceCommand.InstallProfile(device, profile)
        push.push_notification(device)


def build_custom_preference_profile(device):
    content = { }

    groups = device.all_groups()
    groups.sort(key=lambda group: group.priority)
    for group in groups:
        prefs = DeviceGroupManagedPreference.objects.filter(group=group)
        for pref in prefs:
            build_custom_preference_profile_pref(content, pref)

    prefs = DeviceManagedPreference.objects.filter(device=device)
    for pref in prefs:
        build_custom_preference_profile_pref(content, pref)

    return content


def build_custom_preference_profile_pref(content, pref):
    plist = plistlib.readPlistFromString(pref.plist)

    for freq in ['Once', 'Often', 'Always']:
        if len(plist[freq]) == 0:
            continue

        data = dict()
        data['mcx_preference_settings'] = plist[freq]
        if freq == 'Once':
            data['mcx_data_timestamp'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            key = 'Set-Once'
        elif freq == 'Often':
            key = 'Set-Once'
        else:
            key = 'Forced'

        if pref.identifier not in content:
            content[pref.identifier] = { }
        if key not in content[pref.identifier]:
            content[pref.identifier][key] = [ ]

        content[pref.identifier][key].append(data)

