from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='to_url')
@stringfilter
def to_url(value):
    return value + '/'