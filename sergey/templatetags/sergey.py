# coding: utf-8
from __future__ import unicode_literals

from django.conf import settings
from django import template
from django.utils.html import mark_safe
import markdown

register = template.Library()


@register.simple_tag
def header(*args):
    """Function that generates the page title."""
    if not args:
        return settings.SITE_TITLE
    s = ''.join(args)
    if len(s) > 80:
        s = s[:80] + '...'
    return '%s - %s' % (s, settings.SITE_TITLE)


@register.filter
def md(text):
    """Filter that converts Markdown text -> HTML."""
    return mark_safe(
        markdown.markdown(
            text,
            output_format='html5',
            extensions=['sergey.urlize', 'nl2br'],
            safe_mode='replace',
            html_replacement_text='[HTML REMOVED]'
        )
    )
