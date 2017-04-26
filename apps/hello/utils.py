# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from PIL import Image
import json
import logging

logger = logging.getLogger(__name__)


def remove_photo(photo):
    filename = photo.path
    if os.path.exists(filename):
        os.remove(filename)
        logger.info('%s has been removed' % filename)


def user_directory_path(instance, filename):
    return 'person_photo/{1}_{2}'.format(
        instance.id,
        instance.name,
        filename
    )


def resize_photo(instance):
    size = (200, 200)
    filename = instance.photo.path
    if os.path.exists(filename):
        image = Image.open(filename)
        image.thumbnail(size, Image.ANTIALIAS)
        image.save(filename)


def return_json_response(person):
    resp = dict()
    resp['status'] = 'OK'
    if person and person.photo:
        resp['person_photo'] = person.photo.url
    json_resp = json.dumps(resp)
    return json_resp


def return_json_errors(form):
    dict_err = dict()
    for field in form.errors:
        dict_err[field] = form.errors[field].as_text()
    json_resp = json.dumps(dict_err)
    return json_resp
