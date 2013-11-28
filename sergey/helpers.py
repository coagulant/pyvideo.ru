# coding: utf-8
from django.conf import settings
from jingo import register
from jinja2 import Markup
import markdown


@register.function
def header(s=None):
    """Function that generates the page title."""
    if s is None:
        return settings.SITE_TITLE
    if len(s) > 80:
        s = s[:80] + u'...'
    return u'%s - %s' % (s, settings.SITE_TITLE)


@register.filter
def md(text):
    """Filter that converts Markdown text -> HTML."""
    return Markup(
        markdown.markdown(
            text,
            output_format='html5',
            extensions=['sergey.urlize', 'nl2br'],
            safe_mode='replace',
            html_replacement_text='[HTML REMOVED]'))
