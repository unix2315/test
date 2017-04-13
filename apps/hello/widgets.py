from django.forms import widgets


class MyCalendar(widgets.TextInput):

    class Media:
        css = {'all': (
            (
                "http://ajax.googleapis.com" +
                "/ajax/libs/jqueryui/1.8/themes" +
                "/base/jquery-ui.css"),
            )}
        js = (
            'https://code.jquery.com/jquery-1.12.4.js',
            'js/jquery-ui.min.js',
            'js/datepicker.js'
        )
