from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

import html5lib
from html5lib import sanitizer

@register.filter
@stringfilter
def sanitize(data):
    """
    Remove unsafe markup and css from user-generated content,
    retaining only whitelisted constructs.

    TODO: allow specific html tags and attributes as needed
    (e.g. spans with style=color:#[0-9a-fA-F]{3-6})
    """
    p = html5lib.HTMLParser(tokenizer=sanitizer.HTMLSanitizer)
    return mark_safe(p.parseFragment(data).toxml())

