from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.utils import timezone
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
import json

from models import Machine, Fact, HistoricalFact


@csrf_exempt
def submit(request):
    if request.method == 'POST':
        submit = request.POST
    elif request.method == 'GET':
        submit = request.GET
    else:
        raise Http404

    mac = submit.get('mac')
    machine = None
    if mac:
        try:
            machine = Machine.objects.get(mac=mac)
        except Machine.DoesNotExist:
            machine = Machine(mac=mac)

    if machine:
        if submit.get('hostname'):
            machine.hostname = submit.get('hostname')
        machine.last_checkin = timezone.now()
        machine.save()

        response = ''

        facts = submit.get('Facts')
        if facts is not None:
            facts = json.loads(facts)
            for key in facts:
                try:
                    fact = Fact.objects.get(machine=machine, name=key)
                except:
                    fact = Fact(machine=machine, name=key)
                fact.last_update = timezone.now()
                fact.value = facts[key]

                fact.save()

        facts = submit.get('HistoricalFacts')
        if facts is not None:
            facts = json.loads(facts)
            for key in facts:
                fact = HistoricalFact(machine=machine, name=key)
                fact.timestamp = timezone.now()
                fact.value = facts[key]

                fact.save()

        return HttpResponse('Report submitted.\n')

    return HttpResponse('Report not submitted.\n')
