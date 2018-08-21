from django import template
from collections import OrderedDict
register = template.Library()


@register.simple_tag
def get_data(key,value):

    keys= list(key.keys())
    if value in keys:
        if not key[value]=='':
            return key[value]
        else:
            return 0
    else: return 0


    # res = [i for i in value if type(i) == tuple and type(i[1])==OrderedDict ]
    # if res : return True
    # else:return False
    # return "{}".format(value).isdigit()