# coding: utf-8
from django.conf import settings
from jingo import register


@register.function
def header(s=None):
    """Function that generates the page title."""
    if s is None:
        return settings.SITE_TITLE
    if len(s) > 80:
        s = s[:80] + u'...'
    return u'%s - %s' % (s, settings.SITE_TITLE)