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
    last_edit_req = RequestsLog.objects.order_by('edit_time').last()
    if request.is_ajax():
        ajax_resp_obj = {}
        if request.GET['last_edit_time'] != '':
            last_edit_time = parse_datetime(
                request.GET['last_edit_time']
            )
            if not (
                requests
                .filter(edit_time__gt=last_edit_time)
                .exists()
            ):
                ajax_resp_obj = json.dumps(ajax_resp_obj)
                return HttpResponse(
                    ajax_resp_obj,
                    content_type='application/json'
                )
        req_arr = []
        last_requests = requests[:10]
        for req in last_requests:
            req_arr.append({
                'id': req.id,
                'request_time': str(req.request_time.isoformat()),
                'path': req.path,
                'status_code': req.status_code,
                'method': req.method,
                'priority': req.priority
                })
        ajax_resp_obj['ajaxReqArr'] = req_arr
        if last_edit_req:
            ajax_resp_obj['lastEditTime'] = last_edit_req.edit_time.isoformat()
        ajax_resp_obj = json.dumps(ajax_resp_obj)
        return HttpResponse(ajax_resp_obj, content_type='application/json')
    last_requests = requests[:10]
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
