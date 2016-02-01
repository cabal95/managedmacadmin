from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from models import AppInventoryItem, Device, DeviceManagedPreference, DeviceGroup, DeviceGroupManagedPreference
from datetime import datetime, timedelta
import plistlib
import uuid
import mcx
import json


@login_required
def index(request):
    if request.method == 'GET':
        data = request.GET
    else:
        data = request.POST
            
    result = { }
    if 'command' in data:
        if data['command'] == 'create':
            if DeviceGroup.objects.filter(name=data['name']).count() > 0:
                result['status'] = 'ERROR'
                result['error'] = 'Name exists.'
                return HttpResponse(json.dumps(result))

            group = DeviceGroup(name=data['name'], uuid=str(uuid.uuid4()))
            group.save()

            result['status'] = 'OK'
            result['id'] = group.uuid
        elif data['command'] == 'delete':
            if DeviceGroup.objects.filter(uuid=data['id']).count() == 0:
                result['status'] = 'ERROR'
                result['error'] = 'Not found.'
                return HttpResponse(json.dumps(result))

            group = DeviceGroup.objects.get(uuid=data['id'])
            group.delete()

            result['status'] = 'OK'
            result['id'] = data['id']
        else:
            result['status'] = 'ERROR'
            result['error'] = 'Invalid request'

        return HttpResponse(json.dumps(result))

    groups = DeviceGroup.objects.all()
    context = {
        'groups': groups,
    }

    return render(request, 'mdm/groups/index.html', context)


@login_required
def detail(request, id):
    group = None
    try:
        group = DeviceGroup.objects.get(uuid=id)
    except DeviceGroup.DoesNotExist:
        raise Http404

    prefs = DeviceGroupManagedPreference.objects.filter(group=group)
    preflist = [ ]
    for pref in prefs:
        app = AppInventoryItem.objects.filter(identifier=pref.identifier).first()
        item = { 'identifier': pref.identifier }
        if app:
            item['name'] = app.name
        else:   
            item['name'] = pref.identifier
        preflist.append(item)

    context = {
        'group': group,
        'preferences': preflist,
    }

    return render(request, "mdm/groups/detail.html", context)


@login_required
def api(request, id):
    group = None
    try:
        group = DeviceGroup.objects.get(uuid=id)
    except DeviceGroup.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        data = request.GET
    else:
        data = request.POST

    result = { }
    if 'command' not in data:
        result['status'] = 'ERROR'
        result['error'] = 'Invalid request';
    elif data['command'] == 'set':
        attribute = data['attribute']
        value = data['value']
        if attribute == 'name':
            group.name = value
            group.save()
            result['status'] = 'OK'
        elif attribute == 'description':
            group.description = value
            group.save()
            result['status'] = 'OK'
        elif attribute == 'priority':
            result['status'] = 'OK'
            try:
                group.priority = value
                group.save()
            except:
                result['status'] = 'ERROR';
                result['error'] = 'Could not parse value into integer.'
        else:
            result['status'] = 'ERROR'
            result['error'] = 'Unknown attribute'
    elif data['command'] == 'addDevices':
        result['items'] = [ ]
        for id in data['id'].split(','):
            device = Device.objects.get(udid=id)
            if not device in group.devices.all():
                group.devices.add(device)
                mcx.build_system_configuration_profile(device, install=True)
                result['items'].append({ 'name': device.name, 'id': device.udid })
        group.save()
        result['status'] = 'OK'
    elif data['command'] == 'addGroups':
        result['items'] = [ ]
        for id in data['id'].split(','):
            g = DeviceGroup.objects.get(uuid=id)
            if not g in group.groups.all():
                group.groups.add(g)
                result['items'].append({ 'name': g.name, 'id': g.uuid })
        group.save()
        for device in group.devices.all():
            mcx.build_system_configuration_profile(device, install=True)
        result['status'] = 'OK'
    elif data['command'] == 'addPreference':
        if DeviceGroupManagedPreference.objects.filter(group=group, identifier=data['identifier']).count() > 0:
            result['status'] = 'ERROR'
            result['error'] = 'Identifier exists.'
            return HttpResponse(json.dumps(result))

        pref = DeviceGroupManagedPreference(group=group, identifier=data['identifier'])
        pref.plist = '<plist><dict><key>Once</key><dict /><key>Often</key><dict /><key>Always</key><dict /></dict></plist>'
        pref.save()

        result['status'] = 'OK'
        result['identifier'] = pref.identifier
        result['url'] = reverse('devicegroup_preference_edit', args=(group.uuid, pref.identifier,))
    elif data['command'] == 'removeDevice':
        device = Device.objects.get(udid=data['id'])
        if device in group.devices.all():
            group.devices.remove(device)
            group.save()
            mcx.build_system_configuration_profile(device, install=True)
        result['status'] = 'OK'
    elif data['command'] == 'removeGroup':
        g = DeviceGroup.objects.get(uuid=data['id'])
        if g in group.groups.all():
            group.groups.remove(g)
            group.save()
        for device in group.devices.all():
            mcx.build_system_configuration_profile(device, install=True)
        result['status'] = 'OK'
    elif data['command'] == 'removePreference':
        if DeviceGroupManagedPreference.objects.filter(group=group, identifier=data['identifier']).count() == 0:
            result['status'] = 'ERROR'
            result['error'] = 'Identifier not found.'
            return HttpResponse(json.dumps(result))

        pref = DeviceGroupManagedPreference.objects.get(group=group, identifier=data['identifier'])
        pref.delete()

        result['status'] = 'OK'
        result['identifier'] = data['identifier']
    elif data['command'] == 'availableDevices':
        devices = Device.objects.filter(name__startswith=data['query'])
        result['items'] = [ ]
        for device in devices:
            result['items'].append({ 'name': device.name, 'id': device.udid })
        result['status'] = 'OK'
    elif data['command'] == 'availableGroups':
        groups = DeviceGroup.objects.filter(name__startswith=data['query'])
        result['items'] = [ ]
        for g in groups:
            result['items'].append({ 'name': g.name, 'id': g.uuid })
        result['status'] = 'OK'
    else:
        result['status'] = 'ERROR'
        result['error'] = 'Unknown command'

    return HttpResponse(json.dumps(result))


