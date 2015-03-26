from functools import wraps

from django.utils.translation import ugettext as _

def tuplify(a_generator):
    @wraps(a_generator)
    def wrapper(*args, **kwargs):
        return tuple(sorted(each for each in a_generator(*args, **kwargs)))
    return wrapper

@tuplify
def choices(an_enum):
    """Usage:
    class SomethingChoices(object):
        BAR, BAZ = range(2)
    examle_field = django.db.models.SomeFieldType(choices=choices(SomethingChoices))"""
    # REFACT: constant ui names should probably be translatable
    # REFACT: consider to humanize() the display names
    for constant in dir(an_enum):
        if constant.isupper():
            yield (getattr(an_enum, _(constant)), constant)

