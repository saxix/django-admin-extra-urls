import re
from itertools import chain

from django import template
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.template import Node, TemplateSyntaxError

register = template.Library()


@register.assignment_tag(takes_context=True)
def has_permission(context, perm_name):
    if not perm_name:
        return True
    request = context['request']
    user = request.user
    if callable(perm_name):
        try:
            return perm_name(request, context.get('original', None))
        except PermissionDenied:
            return False
    else:
        return user.has_perm(perm_name)


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


class ExtraUrlNode(Node):
    def __init__(self, methodname, varname, target):
        self.methodname = methodname
        self.varname = varname
        self.object = target

    def render(self, context):
        methodname = template.Variable(self.methodname).resolve(context)
        target = template.Variable(self.object).resolve(context)

        model_admin = context['adminform'].model_admin
        for name, options in chain(model_admin.extra_detail_buttons, model_admin.extra_buttons):
            if name == methodname:
                opts = options._asdict()
                if target:
                    opts['href'] = reverse(admin_urlname(target._meta, methodname),
                                           args=[target.pk])
                context[self.varname] = opts
                return ''
        raise TemplateSyntaxError("'%s' is not a valid extra url name" % target)


@register.tag
def extraurl(parser, token):
    """
    Usages:

           {% extraurl 'transitions' as options for adminform.form.instance %}
            <li><a href="{{ options.href }}" class="{{ options.css_class }}"><i
                class="{{ options.icon }} icon-alpha75"></i>{{ options.label }}</a>
            </li>

    :param parser:
    :param token:
    :return:
    """
    bits = token.contents.split()
    target = None
    if len(bits) not in [4, 6]:
        raise TemplateSyntaxError("extraurl require five or six arguments. %s passed" % len(bits))
    if bits[2] != 'as':
        raise TemplateSyntaxError("third argument to the extraurl tag must be 'as'")

    if len(bits) == 6:
        if bits[4] != 'for':
            raise TemplateSyntaxError("fifth argument to the extraurl tag must be 'for'. (not '%s'" % bits[5])
        target = bits[5]

    return ExtraUrlNode(bits[1], bits[3], target)
