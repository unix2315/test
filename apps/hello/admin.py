from django.contrib import admin
from apps.hello.models import Person, RequestsLog, ModelsLog


class PersonAdmin(admin.ModelAdmin):
    pass


class RequestsAdmin(admin.ModelAdmin):
    pass


class ModelsLogAdmin(admin.ModelAdmin):
    pass


admin.site.register(Person, PersonAdmin)
admin.site.register(RequestsLog, RequestsAdmin)
admin.site.register(ModelsLog, ModelsLogAdmin)
