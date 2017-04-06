from django.contrib import admin
from apps.hello.models import Person, RequestsLog


class PersonAdmin(admin.ModelAdmin):
    pass


class RequestsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Person, PersonAdmin)
admin.site.register(RequestsLog, RequestsAdmin)
