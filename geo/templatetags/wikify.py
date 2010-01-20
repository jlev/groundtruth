import re
from django import template
from django.utils.http import urlquote
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
register = template.Library()

@register.filter
@stringfilter
def wikify(value):
    """
    Converts spaces to underscores and then urlquotes.
    For use with Wikipedia style links
    """
    value = urlquote(value)
    return mark_safe(re.sub('[-\s]+', '_', value))