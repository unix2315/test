# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from apps.hello.models import Person, RequestsLog
from django.utils.dateparse import parse_datetime
from apps.hello.forms import EditForm
from django.contrib import messages
import json
from apps.hello.utils import return_json_response
from apps.hello.utils import return_json_errors
from django.contrib.auth.decorators import login_required


def home_view(request):
    person = Person.objects.first()
    context = {'person': person}
    return render(request, 'hello/home_page.html', context)


def requests_view(request):
    requests = RequestsLog.objects.all()
    if request.is_ajax():
        if request.GET['last_edit_time'] != '':
            last_edit_time = parse_datetime(
                request.GET['last_edit_time']
            )
            last_requests = (
                requests.filter(request_time__gt=last_edit_time)[:10]
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
    last_edit_req = RequestsLog.objects.order_by('edit_time').last()
    context = {'requests': last_requests, 'last_edit_req': last_edit_req}
    return render(request, 'hello/requests_page.html', context)


@login_required
def edit_view(request):
    person = Person.objects.first()
    edit_form = EditForm(instance=person)
    context = dict()
    if request.method == 'POST':
        edit_form = EditForm(request.POST, request.FILES, instance=person)
        if edit_form.is_valid():
            edit_form.save()
            if request.is_ajax():
                json_resp = return_json_response(person)
                return HttpResponse(json_resp)
            messages.add_message(
                request,
                messages.INFO,
                "Form submit successfully!"
            )
        if request.is_ajax():
            json_resp = return_json_errors(edit_form)
            return HttpResponse(json_resp)
    if person and person.photo:
        context['person_photo'] = person.photo.url
    context['form'] = edit_form
    return render(request, 'hello/edit_page.html', context)
