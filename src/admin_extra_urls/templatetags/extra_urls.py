import re

from django import template
from django.utils.http import urlencode

from admin_extra_urls.extras import ExtraUrlOptions

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
def eval_extra_options(context, method_name, attrs):
    ret = attrs._asdict()
    obj = context.get('original', None)
    request = context['request']
    user = request.user
    ret['method'] = method_name
    ret['querystring'] = get_preserved_filters(request)

    if callable(attrs.visible):
        ret['visible'] = attrs.visible(obj)
    if ret['perm'] is None:
        ret['authorized'] = True
    elif callable(ret['perm']):
        # try:
        ret['authorized'] = ret['perm'](request, obj)
        # except PermissionDenied:
        #     ret['authorized'] = False
    else:
        ret['authorized'] = user.has_perm(ret['perm'])
    return ExtraUrlOptions(**ret)
