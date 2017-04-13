# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from PIL import Image


def remove_unused_photo(instance, exist_person):
    exist_photo = exist_person.photo
    if exist_photo:
        if (
            not instance.photo or
            exist_photo.path !=
            instance.photo.path
        ):
            exist_filename = exist_photo.path
            if os.path.exists(exist_filename):
                os.remove(exist_filename)


def user_directory_path(instance, filename):
    return 'person_{0}/{1}/{2}'.format(
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
