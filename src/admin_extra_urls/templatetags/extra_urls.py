import re

from django import template

from ..config import Button

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


@register.simple_tag(takes_context=True)
def bind(context, attrs: Button):
    attrs.bind(context)
    return attrs
