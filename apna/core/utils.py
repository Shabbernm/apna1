import random
import string
from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def random_number_generator(size=10, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None, size=10):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=size)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def unique_number_generator(instance, new_number=None, size=10):
    if new_number is not None:
        number = new_number
    else:
        number = random_number_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=number).exists()
    if qs_exists:
        new_number = "{newnumber}".format(
                    newnumber=random_number_generator(size=size)
                )
        return unique_number_generator(instance, new_number=new_number)
    return number