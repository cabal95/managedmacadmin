from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from models import Device, DeviceManagedPreference, DeviceGroup, DeviceGroupManagedPreference
from datetime import datetime, timedelta
import plistlib
import uuid
import mcx
import json


@csrf_exempt
def device(request, udid, ident):
    try:
        device = Device.objects.get(udid=udid)
    except:
        raise Http404

    if request.method == 'GET':
        data = request.GET
    else:
        data = request.POST

    if 'command' in data:
        return device_api(request, data, device, ident)

    context = {
        'device': device,
        'identifier': ident,
    }

    return render(request, 'mdm/preferences/device.html', context)


def device_api(request, data, device, ident):
    command = data['command']

    response = { }
    if command == 'get':
        pref = DeviceManagedPreference.objects.get(device=device, identifier=ident)
        try:
            pref = DeviceManagedPreference.objects.get(device=device, identifier=ident)
            plist = pref.plist
        except:
            plist = '<plist><dict><key>Once</key><dict /><key>Often</key><dict /><key>Always</key><dict /></dict></plist>'

        response['status'] = 'OK'
        response['data'] = plist
    elif command == 'set':
        try:
            pref = DeviceManagedPreference.objects.get(device=device, identifier=ident)
        except:
            pref = DeviceManagedPreference(device=device, identifier=ident)

        pref.plist = data['plist']
        pref.save()

        mcx.build_system_configuration_profile(device, install=True)

        response['status'] = 'OK'
    else:
        response['status'] = 'ERROR'
        response['error'] = 'Unknown command'

    return HttpResponse(json.dumps(response))


@csrf_exempt
def devicegroup(request, id, ident):
    try:
        group = DeviceGroup.objects.get(uuid=id)
    except:
        raise Http404

    if request.method == 'GET':
        data = request.GET
    else:
        data = request.POST

    if 'command' in data:
        return devicegroup_api(request, data, group, ident)

    context = {
        'group': group,
        'identifier': ident,
    }

    return render(request, 'mdm/preferences/devicegroup.html', context)


def devicegroup_api(request, data, group, ident):
    command = data['command']

    response = { }
    if command == 'get':
        try:
            pref = DeviceGroupManagedPreference.objects.get(group=group, identifier=ident)
            plist = pref.plist
        except:
            plist = '<plist><dict><key>Once</key><dict /><key>Often</key><dict /><key>Always</key><dict /></dict></plist>'

        response['status'] = 'OK'
        response['data'] = plist
    elif command == 'set':
        try:
            pref = DeviceGroupManagedPreference.objects.get(group=group, identifier=ident)
        except:
            pref = DeviceGroupManagedPreference(group=group, identifier=ident)

        pref.plist = data['plist']
        pref.save()

        for device in group.recursive_devices():
            mcx.build_system_configuration_profile(device, install=True)

        response['status'] = 'OK'
    else:
        response['status'] = 'ERROR'
        response['error'] = 'Unknown command'

    return HttpResponse(json.dumps(response))


