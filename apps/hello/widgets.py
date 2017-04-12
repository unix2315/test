from django.forms import widgets


class MyCalendar(widgets.TextInput):

    class Media:
        css = {'all': ('css/jquery-ui.min.css',)}
        js = ('js/datepicker.js',)
