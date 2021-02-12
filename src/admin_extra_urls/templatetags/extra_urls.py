import re

from django import template
from django.utils.http import urlencode

register = template.Library()


class NewlinelessNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        return self.remove_newlines(self.nodelist.render(context).strip())

    def remove_newlines(self, value):
        value = re.sub(r'\n', ' ', value)
        value = re.sub(r'\s+', ' ', value)
        return value


@register.tag
def nlless(parser, token):
    """
    Remove all whitespace except for one space from content
    """
    nodelist = parser.parse(('endnlless',))
    parser.delete_first_token()
    return NewlinelessNode(nodelist)


@register.filter
def default_if_empty(v, default):
    if v and v.strip():
        return v
    return default


def get_preserved_filters(request, **extras):
    filters = request.GET.get('_changelist_filters', '')
    if filters:
        preserved_filters = request.GET.get('_changelist_filters')
    else:
        preserved_filters = request.GET.urlencode()

    if preserved_filters:
        return urlencode({'_changelist_filters': preserved_filters})
    return ''


@register.simple_tag(takes_context=True)
def bind(context, attrs):
    attrs.bind(context)
    return attrs
