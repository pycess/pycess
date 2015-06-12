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

from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
class AddInlineEditLinkMixin(object):
    "Needs to be inherited from BEFORE admin.*Inline"
    readonly_fields = ['edit_details']
    edit_label = "Edit"
    def edit_details(self, obj):
        if obj.id:
            opts = self.model._meta
            return mark_safe("<a href='%s'>%s</a>" % (reverse(
                'admin:%s_%s_change' % (opts.app_label, opts.object_name.lower()),
                args=[obj.id]
            ), self.edit_label))
        else:
            return "(save to edit details)"
    edit_details.allow_tags = True

from django.contrib.auth.decorators import login_required
class LoginRequiredMixin(object):
    "needs to be inherited from _before_ django.views.generic.View, or it won't work"
    @classmethod
    def as_view(cls):
        return login_required(super(LoginRequiredMixin, cls).as_view())

