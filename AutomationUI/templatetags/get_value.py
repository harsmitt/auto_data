from django import template
from collections import OrderedDict
register = template.Library()


@register.filter
def get_value(value):

    res = [i for i in value if type(i) == tuple and type(i[1])==OrderedDict ]
    if res : return True
    else:return False
    # return "{}".format(value).isdigit()