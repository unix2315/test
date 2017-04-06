# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from apps.hello.models import Person, RequestsLog
import json
from django.utils.dateparse import parse_datetime


def home_view(request):
    person = Person.objects.first()
    context = {'person': person}
    return render(request, 'hello/home_page.html', context)


def requests_view(request):
    requests = RequestsLog.objects.all()
    if request.is_ajax():
        if request.GET['last_request_time'] != '':
            last_request_time = parse_datetime(
                request.GET['last_request_time']
            )
            last_requests = (
                requests.filter(request_time__gt=last_request_time)[:10]
            )
        else:
            last_requests = requests[:10]
        context = []
        for req in last_requests:
            context.append({
                'id': req.id,
                'request_time': str(req.request_time.isoformat()),
                'path': req.path,
                'status_code': req.status_code,
                'method': req.method
                })
        context = json.dumps(context)
        return HttpResponse(context, content_type='application/json')
    last_requests = requests[:10]
    context = {'requests': last_requests}
    return render(request, 'hello/requests_page.html', context)
