# -*- coding: utf-8 -*-
from django.forms import ModelForm, Textarea
from django.forms import TextInput, DateInput, EmailInput
from apps.hello.models import Person


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
            'date_of_birth': DateInput(attrs={
                'class': 'form-control',
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
