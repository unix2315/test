# -*- coding: utf-8 -*-
from django.shortcuts import render
from apps.hello.models import Person


def home_view(request):
    person = Person.objects.first()
    context = {'person': person}
    return render(request, 'hello/home_page.html', context)


def requests_view(request):
    return render(request, 'hello/requests_page.html')
