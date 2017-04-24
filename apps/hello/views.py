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
from django.views.generic import ListView, TemplateView
from django.views.generic import CreateView, FormView
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator


def home_view(request):
    person = Person.objects.first()
    context = {'person': person}
    return render(request, 'hello/home_page.html', context)


class HomeView(TemplateView):
    template_name = 'hello/home_page.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['person'] = Person.objects.first()
        return context


class RequestsView(ListView):
    model = RequestsLog
    template_name = 'hello/requests_page.html'
    context_object_name = 'requests'
    queryset = RequestsLog.objects.all()[:10]
    last_edit_req = None

    def dispatch(self, *args, **kwargs):
        self.last_edit_req = RequestsLog.objects.order_by('edit_time').last()
        return super(RequestsView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RequestsView, self).get_context_data(**kwargs)
        context['last_edit_req'] = self.last_edit_req
        return context

    def get_json_resp_obj(self):
        ajax_resp_obj = {}
        req_arr = []
        for req in self.get_queryset():
            req_arr.append({
                'id': req.id,
                'request_time': str(req.request_time.isoformat()),
                'path': req.path,
                'status_code': req.status_code,
                'method': req.method,
                'priority': req.priority
                })
        ajax_resp_obj['ajaxReqArr'] = req_arr
        if self.last_edit_req:
            ajax_resp_obj['lastEditTime'] = \
                self.last_edit_req.edit_time.isoformat()
        ajax_resp_obj = json.dumps(ajax_resp_obj)
        return ajax_resp_obj

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            ajax_resp_obj = {}
            if request.GET['last_edit_time'] != '':
                last_edit_time = parse_datetime(
                    request.GET['last_edit_time']
                )
                if not (
                    RequestsLog.objects
                    .filter(edit_time__gt=last_edit_time)
                    .exists()
                ):
                    ajax_resp_obj = json.dumps(ajax_resp_obj)
                    return HttpResponse(
                        ajax_resp_obj,
                        content_type='application/json'
                    )
            ajax_resp_obj = self.get_json_resp_obj()
            return HttpResponse(ajax_resp_obj, content_type='application/json')
        return super(RequestsView, self).get(request, **kwargs)

    def post(self, request, *args, **kwargs):
        for req in request.POST:
            if req and req != 'csrfmiddlewaretoken':
                req_obj = RequestsLog.objects.get(id=req)
                req_obj.priority = request.POST[req]
                req_obj.save()
        if request.is_ajax():
            ajax_resp_obj = self.get_json_resp_obj()
            return HttpResponse(ajax_resp_obj, content_type='application/json')
        return super(RequestsView, self).get(request, **kwargs)


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


class EditView(FormView):
    form_class = EditForm
    template_name = 'hello/edit_page.html'
    instance = None

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EditView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('hello:edit_page')

    def form_valid(self, form):
        if form.has_changed():
            form.save()
        self.instance = Person.objects.first()
        if self.request.is_ajax():
            json_resp = return_json_response(self.instance)
            return HttpResponse(json_resp)
        messages.add_message(
            self.request,
            messages.INFO,
            "Form submit successfully!"
        )
        return super(EditView, self).form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            json_resp = return_json_errors(form)
            return HttpResponse(json_resp)
        return super(EditView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(EditView, self).get_context_data(**kwargs)
        self.instance = Person.objects.first()
        if self.instance and self.instance.photo:
            context['person_photo'] = self.instance.photo.url
        return context

    def get_form_kwargs(self):
        kwargs = super(EditView, self).get_form_kwargs()
        self.instance = Person.objects.first()
        if self.instance is not None:
            kwargs.update({'instance': self.instance})
        return kwargs


class CreatePersonView(CreateView):
    model = Person
    form_class = EditForm
    template_name = 'hello/edit_page.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreatePersonView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('hello:edit_page', kwargs={'pk': self.object.id})
