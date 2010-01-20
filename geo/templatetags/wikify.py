from django import template

register = template.Library()

@register.filter
@stringfilter
def wikify(value):
    """
    Normalizes string, removes non-alpha characters,
    and converts spaces to +.
    For use with Wikipedia style links
    """
    import unicodedata
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return mark_safe(re.sub('[-\s]+', '+', value))
wikify.is_safe = True