from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from datetime import datetime, timedelta
from models import Certificate, CertificateAuthority
from socket import getfqdn
import base64
import mdm.geo
import json
import OpenSSL


@login_required
def index(request):
    ca = CertificateAuthority.objects.filter(revoked=False).first()

    context = {
        'ca': ca,
    }

    return render(request, 'config/index.html', context)


@login_required
def generateCA(request):
    if request.method == 'GET':
        data = request.GET
    else:
        data = request.POST

    if 'command' in data:
        result = { }
        if data['command'] == 'generate':
            key = OpenSSL.crypto.PKey()
            key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)
            ca = OpenSSL.crypto.X509()
            ca.set_version(2)
            ca.set_serial_number(1)
            ca.get_subject().C = data['country']
            ca.get_subject().ST = data['state']
            ca.get_subject().L = data['city']
            ca.get_subject().O = data['org']
            ca.get_subject().OU = data['orgunit']
            ca.get_subject().CN = data['name']
            ca.gmtime_adj_notBefore(0)
            ca.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
            ca.set_issuer(ca.get_subject())
            ca.set_pubkey(key)
            ca.add_extensions([
                OpenSSL.crypto.X509Extension("basicConstraints", True, "CA:TRUE, pathlen:0"),
                OpenSSL.crypto.X509Extension("keyUsage", True, "digitalSignature,keyCertSign"),
#                OpenSSL.crypto.X509Extension("subjectKeyIdentifier", False, "hash", subject=ca),
            ])
#            ca.add_extensions([
#                OpenSSL.crypto.X509Extension("authorityKeyIdentifier", False, "keyid:always", issuer=ca),
#            ])
            ca.sign(key, "sha256")

            cert = CertificateAuthority()
            cert.key = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key)
            cert.crt = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, ca)
            cert.date_created = datetime.now()
            cert.save()

            result['status'] = 'OK'
        else:
            result['status'] = 'ERROR'
            result['error'] = 'Invalid command'

        return HttpResponse(json.dumps(result))

    context = {
        'org': settings.ORGANIZATION,
        'geo': mdm.geo.geocode(''),
    }

    return render(request, 'config/generateCA.html', context)

