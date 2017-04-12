# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def user_directory_path(instance, filename):
    return 'person_{0}/{1}/{2}'.format(
        instance.id,
        instance.name,
        filename
    )
