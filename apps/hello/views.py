# -*- coding: utf-8 -*-
from django.shortcuts import render


def home_view(request):
    return render(request, 'hello/home_page.html')
