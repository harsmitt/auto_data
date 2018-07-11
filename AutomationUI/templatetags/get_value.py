from django import template
from collections import OrderedDict
register = template.Library()


@register.filter
def get_value(value):

    if type(value)==OrderedDict:
        return True
    else:
        return False