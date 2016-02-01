from django.conf import settings
from django.db import transaction
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, Http404
from models import Device, DeviceCommand, AppInventoryItem, DeviceCheckin, DeviceManagedPreference, ProfileInventoryItem, DeviceProfile, DeviceGroup, DeviceGroupManagedPreference
from config.models import CertificateAuthority, Certificate
import geo
import commands
import standard_commands
from datetime import datetime, timedelta
import base64
import plistlib
import logging
import push
import uuid
import json
import mcx
from M2Crypto import BIO, X509, SMIME, m2
import OpenSSL
import os
import pprint


@login_required
def index(request):
    devices = Device.objects.all()
    context = {
        'devices': devices,
    }

    return render(request, 'mdm/index.html', context)


@csrf_exempt
@login_required
def monitor_detail_api(request, udid):
    device = None
    if udid:
        try:
            device = Device.objects.get(udid=udid)
        except Device.DoesNotExist:
            raise Http404
    else:
        raise Http404

    if request.method == 'GET':
        data = request.GET
    else:
        data = request.POST

    result = { }
    if 'command' not in data:
        result['status'] = 'ERROR'
        result['error'] = 'Invalid request'
        return HttpResponse(json.dumps(result))

    if data['command'] == 'CommandHistory':
        commands = DeviceCommand.objects.filter(device=device)
        result['objects'] = [ ]
        for cmd in commands:
            obj = {
                'name': cmd.name,
                'status': cmd.get_status_display(),
                'date_requested': cmd.date_requested.strftime("%m/%d/%Y %l:%M%p"),
                'date_requested_sort': cmd.date_requested.strftime("%s"),
            }
            if cmd.date_completed:
                obj['date_completed'] = cmd.date_completed.strftime("%m/%d/%Y %l:%M%p")
                obj['date_completed_sort'] = cmd.date_completed.strftime("%s")
            else:
                obj['date_completed'] = ''
                obj['date_completed_sort'] = -1
       
            result['objects'].append(obj)

        result['status'] = 'OK'
    elif data['command'] == 'InstalledProfiles':
        profiles = ProfileInventoryItem.objects.filter(device=device)
        result['objects'] = [ ]
        for profile in profiles:
            managed = profile.identifier[:len(settings.MANAGED_PROFILE_IDENTIFIER)] == settings.MANAGED_PROFILE_IDENTIFIER
            uptodate = False
            if managed:
                p = DeviceProfile.objects.filter(device=device, identifier=profile.identifier).first()
                if p and p.uuid == profile.uuid:
                    uptodate = True

            result['objects'].append({
                'name': profile.name,
                'description': profile.description,
                'identifier': profile.identifier,
                'uuid': profile.uuid,
                'managed': managed,
                'uptodate': uptodate,
            })
        result['status'] = 'OK'
    elif data['command'] == 'LocationHistory':
        checkins = DeviceCheckin.objects.filter(device=device)
        result['objects'] = [ ]
        for checkin in checkins:
            result['objects'].append({
                'start_date': checkin.start_date.strftime("%m/%d/%Y %l:%M%p"),
                'start_date_sort': checkin.start_date.strftime("%s"),
                'end_date': checkin.end_date.strftime("%m/%d/%Y %l:%M%p"),
                'end_date_sort': checkin.end_date.strftime("%s"),
                'ip': checkin.ip,
                'latitude': checkin.latitude,
                'longitude': checkin.longitude,
                'city': checkin.city,
                'region': checkin.region_code,
                'country': checkin.country_code,
            })
        result['status'] = 'OK'
    elif data['command'] == 'InstallProfile':
        profile = DeviceProfile.objects.filter(device=device, identifier=data['identifier']).first()
        if profile:
            DeviceCommand.InstallProfile(device, profile)
            push.push_notification(device)
            result['status'] = 'OK'
        else:
            result['status'] = 'ERROR'
            result['error'] = 'Invalid profile specified.'

    return HttpResponse(json.dumps(result))


@login_required
def detail(request, udid):
    device = None
    if udid:
        try:
            device = Device.objects.get(udid=udid)
        except Device.DoesNotExist:
            raise Http404
    else:
        raise Http404

    if request.method == 'GET':
        data = request.GET
    else:
        data = request.POST

    if 'command' in data:
        result = { }
        command = data['command']

        if command == 'addGroups':
            result['items'] = [ ]
            for id in data['id'].split(','):
                group = DeviceGroup.objects.get(uuid=id)
                if not device in group.devices.all():
                    group.devices.add(device)
                    group.save()
                    result['items'].append({ 'name': group.name, 'id': group.uuid })
            mcx.build_system_configuration_profile(device, install=True)
            result['status'] = 'OK'
        elif command == 'removeGroup':
            group = DeviceGroup.objects.get(uuid=data['id'])
            if device in group.devices.all():
                group.devices.remove(device)
                group.save()
                mcx.build_system_configuration_profile(device, install=True)
            result['status'] = 'OK'
        elif command == 'availableGroups':
            groups = DeviceGroup.objects.filter(name__startswith=data['query'])
            result['items'] = [ ]
            for g in groups:
                result['items'].append({ 'name': g.name, 'id': g.uuid })
            result['status'] = 'OK'
        elif command == 'ListPreferences':
            result['objects'] = [ ]
            prefs = DeviceManagedPreference.objects.filter(device=device).all()
            for pref in prefs:
                app = AppInventoryItem.objects.filter(identifier=pref.identifier).first()
                item = { 'id': pref.identifier }
                if app:
                    item['name'] = app.name
                else:   
                    item['name'] = pref.identifier
                result['objects'].append(item)
            result['status'] = 'OK'
        elif command == 'removePreference':
            pref = DeviceManagedPreference.objects.get(device=device, identifier=data['id'])
            pref.delete()
            result['status'] = 'OK'
        else:
            result['status'] = 'ERROR'
            result['error'] = 'Invalid request'

        return HttpResponse(json.dumps(result))

    apps_last_updated = None
    obj = DeviceCommand.objects.filter(device=device, type='com.github.managedmacadmin.InstalledApplicationList', status=DeviceCommand.SUCCESS).order_by('-date_completed').first()
    if obj:
        apps_last_updated = obj.date_completed

    profiles_last_updated = None
    obj = DeviceCommand.objects.filter(device=device, type='com.github.managedmacadmin.ProfileList', status=DeviceCommand.SUCCESS).order_by('-date_completed').first()
    if obj:
        profiles_last_updated = obj.date_completed

    context = {
        'device': device,
        'groups': device.devicegroup_set.order_by('-priority', 'name').all(),
        'apps': AppInventoryItem.objects.filter(device=device),
        'apps_last_updated': apps_last_updated,
        'profiles_last_updated': profiles_last_updated,
    }

    return render(request, 'mdm/detail.html', context)
   

@login_required
def send_push(request, udid):
    device = None
    if udid:
        try:
            device = Device.objects.get(udid=udid)
        except Device.DoesNotExist:
            raise Http404
    else:
        raise Http404

    push.push_notification(device)
    return HttpResponse('OK')


@login_required
def device_information(request, udid):
    device = None
    if udid:
        try:
            device = Device.objects.get(udid=udid)
        except Device.DoesNotExist:
            raise Http404
    else:
        raise Http404

    DeviceCommand.NewDeviceInformation(device)

    push.push_notification(device)
    return HttpResponse('OK')


@login_required
def profile_list(request, udid):
    device = None
    if udid:
        try:
            device = Device.objects.get(udid=udid)
        except Device.DoesNotExist:
            raise Http404
    else:
        raise Http404

    DeviceCommand.NewProfileList(device)
    push.push_notification(device)

    return HttpResponse('OK')


@login_required
def application_list(request, udid):
    device = None
    if udid:
        try:
            device = Device.objects.get(udid=udid)
        except Device.DoesNotExist:
            raise Http404
    else:
        raise Http404

    DeviceCommand.NewInstalledApplicationList(device)
    push.push_notification(device)

    return HttpResponse('OK')


@login_required
def install_profile(request, udid):
    device = None
    if udid:
        try:
            device = Device.objects.get(udid=udid)
        except Device.DoesNotExist:
            raise Http404
    else:
        raise Http404

    if device.os != Device.OSX:
        return HttpResponse('ERROR: Invalid Device Type')

    mcx.build_system_configuration_profile(device, install=True)

    return HttpResponse('OK')
   

@csrf_exempt
#@transaction.commit_manually()
def enroll(request):
    if request.method == 'GET':
        data = request.GET
    else:
        data = request.POST

    # Delete any certificates that have not been associated with a
    # device yet and are older than 1 day. TODO: Configurable
    since = datetime.now() - timedelta(days=1)
    Certificate.objects.filter(device=None, date_created__lt=since).delete()

    # If they have not provided a pin or provided the wrong pin, HTML page.
    if 'pin' not in data:
        result = render(request, 'mdm/enroll.html', { })
        transaction.commit()
        return result
    if data['pin'] != settings.ENROLL_PIN:
        result = render(request, 'mdm/enroll.html', { 'invalid': '1' })
        transaction.commit()
        return result

    # Get the CA information
    ca = CertificateAuthority.objects.filter(revoked=False).select_for_update().first()
    ca_key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, ca.key)
    ca_crt = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, ca.crt)

    # Create a new certificate for the client
    key = OpenSSL.crypto.PKey()
    key.generate_key( OpenSSL.crypto.TYPE_RSA, 1024 )
    cert = OpenSSL.crypto.X509()
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
    cert.get_subject().CN = "Client MDM Certificate"
    cert.set_serial_number(ca.next_serial)
    cert.set_pubkey(key)
    cert.set_issuer(ca_crt.get_subject())
    cert.sign(ca_key, "sha256")

    plist = { }
    plist['PayloadDisplayName'] = 'MDM for ' + settings.ORGANIZATION
    plist['PayloadDescription'] = plist['PayloadDisplayName']
    plist['PayloadIdentifier'] = settings.IDENTIFIER + '.mdmprofile'
    plist['PayloadOrganization'] = settings.ORGANIZATION
    plist['PayloadRemovalDisallowed'] = False
    plist['PayloadType'] = 'Configuration'
    plist['PayloadUUID'] = str(uuid.uuid4())
    plist['PayloadVersion'] = 1
    plist['PayloadContent'] = [ ]

    ident = { }
    ident['PayloadDisplayName'] = 'Device Identity'
    ident['PayloadDescription'] = 'Provides device authentication certificate'
    ident['PayloadIdentifier'] = plist['PayloadIdentifier'] + '.credential'
    ident['PayloadOrganization'] = plist['PayloadOrganization']
    ident['PayloadType'] = 'com.apple.security.pkcs12'
    ident['PayloadUUID'] = str(uuid.uuid4())
    ident['PayloadVersion'] = 1
    ident['Password'] = 'k18234ks'
    ident['PayloadCertificateFileName'] = 'credentials.p12'

    mdm = { }
    mdm['PayloadDisplayName'] = 'Mobile Device Management'
    mdm['PayloadDescription'] = 'Configures Mobile Device Management'
    mdm['PayloadIdentifier'] = plist['PayloadIdentifier'] + '.mdm'
    mdm['PayloadOrganization'] = plist['PayloadOrganization']
    mdm['PayloadType'] = 'com.apple.mdm'
    mdm['PayloadUUID'] = str(uuid.uuid4())
    mdm['PayloadVersion'] = 1
    mdm['ServerURL'] = 'https://mdm.highdesertchurch.com/mdm/checkin'
    mdm['CheckInURL'] = mdm['ServerURL']
    mdm['CheckOutWhenRemoved'] = True
    mdm['AccessRights'] = 8191
    mdm['Topic'] = settings.PUSH_TOPIC
    mdm['SignMessage'] = True
    mdm['IdentityCertificateUUID'] = ident['PayloadUUID']

    # Add the private key and certificate to the payload
    p12 = OpenSSL.crypto.PKCS12()
    p12.set_privatekey(key)
    p12.set_certificate(cert)
    ident['PayloadContent'] = plistlib.Data(p12.export(ident['Password']))

    # Save the CA and certificate
    ca.next_serial = ca.next_serial + 1
    ca.save()
    c = Certificate()
    c.key = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key)
    c.crt = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    c.ca = ca
    c.date_created = datetime.now()
    c.md5 = cert.digest('md5').replace(':', '')
    c.serial = cert.get_serial_number()
    c.save()

    # Safe to commit transaction at this point.
    transaction.commit()

    # Assemble final property list and return
    plist['PayloadContent'].append(ident)
    plist['PayloadContent'].append(mdm)

    content = plistlib.writePlistToString(plist)

    # Sign the entire plist data.
    smime = SMIME.SMIME()
    key = BIO.MemoryBuffer(str(ca.key))
    crt = BIO.MemoryBuffer(str(ca.crt))
    smime.load_key_bio(key, crt)
    content_bio = BIO.MemoryBuffer(content)
    data_p7 = smime.sign(content_bio)
    data_bio = BIO.MemoryBuffer()
    data_p7.write_der(data_bio)
    data = data_bio.read()

    return HttpResponse(data, content_type = 'application/x-apple-aspen-config; charset=utf-8')


@csrf_exempt
def checkin(request):
    logger = logging.getLogger('django')
    logger.debug('WWW Query: %s', request.body)

    if settings.USE_CERTIFICATE == True:
        # Get the certificate fingerprint
        try:
            bio = BIO.MemoryBuffer(base64.b64decode(request.META['HTTP_MDM_SIGNATURE']))
            p7 = SMIME.PKCS7(m2.pkcs7_read_bio_der(bio._ptr()), 1)
            stk = X509.X509_Stack()
            sk3 = p7.get0_signers(stk)
            cert = sk3.pop()
            fingerprint = cert.get_fingerprint('md5')
            if len(fingerprint) == 31:
                fingerprint = '0' + fingerprint
        except:
            fingerprint = None

        logger.debug('Fingerprint: %s', fingerprint)
        # If no certificate supplied, permission denied.
        if fingerprint == None and settings.REQUIRE_CERTIFICATE == True:
            return HttpResponseForbidden()

        # If no certificate found, permission denied.
        certificate = Certificate.objects.filter(md5=fingerprint).first()
        if certificate == None and settings.REQUIRE_CERTIFICATE == True:
            return HttpResponseForbidden()

        # If certificate does not match device, permission denied.
        # TODO
    else:
        certificate = None

    # Prepare handling of checkin request and response commands.
    responseData = plistlib.writePlistToString(dict())
    standard_commands.initialize()

    try:
        plist = plistlib.readPlistFromString(request.body)
    except:
        plist = dict()

    if 'MessageType' in plist:
        if plist['MessageType'] == 'Authenticate':
            if 'UserID' in plist:
                return HttpResponseBadRequest('User binding not currently supported')

            device = Device.objects.filter(udid=plist['UDID']).first()
            if device == None:
                device = Device(udid=plist['UDID'], push_topic=plist['Topic'])
            device.last_checkin = datetime.now()
            device.last_notification = datetime.now()
            device.save()
            if certificate != None:
                certificate.device = device
                certificate.save()

            try:
                group = DeviceGroup.objects.filter(uuid=settings.DEFAULT_DEVICE_GROUP).first()
                group.devices.add(device)
                group.save()
            except:
                pass

        elif plist['MessageType'] == 'TokenUpdate':
            if 'UserID' in plist:
                return HttpResponseBadRequest('User binding not currently supported')

            device = Device.objects.get(udid=plist['UDID'])
            device.push_topic = plist['Topic']
            device.push_token = plist['Token'].asBase64(maxlinelength=8000)
            device.push_magic = plist['PushMagic']
            device.last_checkin = datetime.now()
            device.save()

            DeviceCommand.NewDeviceInformation(device)
            DeviceCommand.NewProfileList(device)
            DeviceCommand.NewInstalledApplicationList(device)
            push.push_notification(device)
        elif plist['MessageType'] == 'CheckOut':
            if 'UserID' in plist:
                return HttpResponseBadRequest('User binding not currently supported')

            Device.objects.get(udid=plist['UDID']).delete()
        else:
            print 'Unknown message type: ' + plist['MessageType']
            print plist
    elif 'Status' in plist:
        responseData = ''

        # Update device checkin time
        device = Device.objects.get(udid=plist['UDID'])
        device.last_checkin = datetime.now()
        device.save()

        # Update device location if it has been 15 minutes since last.
        since = datetime.now() - timedelta(minutes=15)
        location = DeviceCheckin.objects.filter(device=device).order_by('-end_date').first()
        if location and location.ip == request.META['REMOTE_ADDR']:
            location.end_date = datetime.now()
            location.save()
        else:
            location = DeviceCheckin(device=device)
            location.start_date = datetime.now()
            location.end_date = datetime.now()
            location.ip = request.META['REMOTE_ADDR']
            loc = geo.geocode(request.META['REMOTE_ADDR'])
            location.latitude = loc['latitude']
            location.longitude = loc['longitude']
            location.country_code = loc['country_code']
            location.region_code = loc['region_code']
            location.city = loc['city']
            if 'country_name' in loc:
                location.country_name = loc['country_name']
            if 'region_name' in loc:
                location.region_name = loc['region_name']
            location.save()

        if plist['Status'] == 'Acknowledged':
            cmd = DeviceCommand.objects.get(uuid=plist['CommandUUID'])
            cmd.status = DeviceCommand.SUCCESS
            cmd.date_completed = datetime.now()
            cmd.save()
            commands.handleCommandResponse(cmd, plist)
        elif plist['Status'] == 'Error' or plist['Status'] == 'CommandFormatError':
            cmd = DeviceCommand.objects.get(uuid=plist['CommandUUID'])
            cmd.status = DeviceCommand.FAILED
            cmd.date_completed = datetime.now()
            cmd.save()
        elif plist['Status'] == 'NotNow':
            cmd = DeviceCommand.objects.get(uuid=plist['CommandUUID'])
            cmd.status = DeviceCommand.PENDING
            cmd.attempts = 0
            cmd.save()

        if plist['Status'] == 'Idle' or plist['Status'] == 'Acknowledged':
            # Look for the next command, mark as failed if too many attempts.
            cmd = DeviceCommand.objects.filter(device=device, status__in=[DeviceCommand.PENDING, DeviceCommand.RUNNING]).first()
            while cmd and cmd.attempts >= 3:
                cmd.status = DeviceCommand.FAILED
                cmd.save()
                cmd = DeviceCommand.objects.filter(device=device, status__in=[DeviceCommand.PENDING, DeviceCommand.RUNNING]).first()

            # Run the next command.
            if cmd:
                data = commands.dataForCommand(cmd)
                responseData = plistlib.writePlistToString(data)
                cmd.status = DeviceCommand.RUNNING
                cmd.attempts += 1
                cmd.save()

    logger.debug('WWW Result: %s', responseData)

    response = HttpResponse(responseData, content_type = 'application/xml; charset=UTF-8')
    response['Content-Length'] = len(responseData)
    return response

