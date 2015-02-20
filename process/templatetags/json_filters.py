from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe
from django.template import Library
import json

register = Library()

@register.filter
def jsonify(object):
    return mark_safe(json.dumps(object, cls=DjangoJSONEncoder))

