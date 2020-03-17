from django import template

register = template.Library()

@register.filter
def get_model_name(object):
    return object.__class__.__name__