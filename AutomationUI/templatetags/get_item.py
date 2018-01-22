from django import template

register = template.Library()


@register.filter
def get_item(value):
    return "{}".format(value).isdigit()