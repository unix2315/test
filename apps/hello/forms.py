# -*- coding: utf-8 -*-
from django.forms import ModelForm, Textarea
from django.forms import TextInput, EmailInput
from apps.hello.models import Person
from apps.hello.widgets import MyCalendar


class EditForm(ModelForm):
    class Meta:
        model = Person
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'required': True
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control',
                'required': True
            }),
            'date_of_birth': MyCalendar(attrs={
                'class': 'form-control datepicker',
                'required': True
            }),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'skype': TextInput(attrs={'class': 'form-control'}),
            'jabber': EmailInput(attrs={'class': 'form-control'}),
            'other_contacts': Textarea(attrs={
                'class': 'form-control',
                'cols': 23,
                'rows': 3
            }),
            'bio': Textarea(attrs={
                'class': 'form-control',
                'cols': 23,
                'rows': 3
            }),
        }
