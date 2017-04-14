from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag
def edit_link(any_object):
    admin_url_name = ('admin:%s_%s_change' % (
        any_object._meta.app_label,
        any_object._meta.model_name
    ))
    return reverse(admin_url_name, args=(any_object.id,))
