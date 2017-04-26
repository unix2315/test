# -*- coding: utf-8 -*-
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
from django.views.generic import FormView
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
import logging


logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = 'hello/home_page.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        person = Person.objects.first()
        if not person:
            logger.info('No person was found')
        context['person'] = person
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


class EditView(FormView):
    form_class = EditForm
    template_name = 'hello/edit_page.html'
    object = None

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EditView, self).dispatch(*args, **kwargs)

    def get_object(self):
        obj = Person.objects.first()
        return obj

    def get_form_kwargs(self):
        kwargs = super(EditView, self).get_form_kwargs()
        self.object = self.get_object()
        if self.object:
            kwargs.update({'instance': self.object})
        return kwargs

    def get_success_url(self):
        return reverse('hello:edit_page')

    def form_valid(self, form):
        if form.has_changed():
            form.save()
            logger.info(
                '%s has changed data in %s field(s)' %
                (self.request.user, form.changed_data)
            )
        self.object = self.get_object()
        if self.request.is_ajax():
            json_resp = return_json_response(self.object)
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
        self.object = self.get_object()
        if self.object and self.object.photo:
            context['person_photo'] = self.object.photo.url
        return context
