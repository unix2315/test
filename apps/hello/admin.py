from django.contrib import admin
from apps.hello.models import Person


class PersonAdmin(admin.ModelAdmin):
    pass

admin.site.register(Person, PersonAdmin)
