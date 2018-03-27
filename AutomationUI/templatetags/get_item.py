from django import template
from collections import OrderedDict
register = template.Library()


@register.filter
def get_item(value):
    # import pdb;pdb.set_trace()
    if type(value) != OrderedDict:
        value=abs(value)
    return "{}".format(value).isdigit()

