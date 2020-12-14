import inspect
import logging
from collections import namedtuple
from functools import update_wrapper

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import re_path, reverse

logger = logging.getLogger(__name__)

IS_GRAPPELLI_INSTALLED = 'grappelli' in settings.INSTALLED_APPS
# ExtraUrlConfig = namedtuple('ExtraUrlConfig', 'path,label,icon,perm,order,css_class,visible')
ExtraUrlOptions = namedtuple('ExtraUrlOptions',
                             'path,querystring,label,icon,perm,order,css_class,visible,authorized,method')
NOTSET = object()


class ActionFailed(Exception):
    pass


def _confirm_action(modeladmin, request,
                    action, message,
                    success_message="",
                    description='',
                    pk=None,
                    extra_context=None,
                    template='admin_extra_urls/confirm.html',
                    error_message=None,
                    **kwargs):
    opts = modeladmin.model._meta
    context = dict(
        modeladmin.admin_site.each_context(request),
        opts=opts,
        app_label=opts.app_label,
        message=message,
        description=description,
        **kwargs)
    if extra_context:
        context.update(extra_context)

    if request.method == 'POST':
        ret = None
        try:
            ret = action(request)
            modeladmin.message_user(request, success_message, messages.SUCCESS)
        except Exception as e:
            modeladmin.message_user(request, error_message or str(e), messages.ERROR)

        return ret or HttpResponseRedirect(reverse(admin_urlname(opts,
                                                                 'changelist')))

    return TemplateResponse(request,
                            template,
                            context)


class ExtraUrlConfigException(RuntimeError):
    pass


class ExtraUrlMixin:
    """
    Allow to add new 'url' to the standard ModelAdmin
    """
    if IS_GRAPPELLI_INSTALLED:  # pragma: no cover
        change_list_template = 'admin_extra_urls/grappelli/change_list.html'
        change_form_template = 'admin_extra_urls/grappelli/change_form.html'
    else:
        change_list_template = 'admin_extra_urls/change_list.html'
        change_form_template = 'admin_extra_urls/change_form.html'

    extra_buttons = []

    def __init__(self, model, admin_site):
        self.extra_actions = []
        # self.extra_detail_actions = []
        super().__init__(model, admin_site)

    def get_urls(self):
        extra_actions = []
        # extra_detail_actions = []
        extra_urls = {}
        for c in inspect.getmro(self.__class__):
            for method_name, method in c.__dict__.items():
                if hasattr(method, 'action'):
                    extra_urls[method_name] = getattr(method, 'action')

        original = super().get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            return update_wrapper(wrapper, view)

        info = [self.model._meta.app_label, self.model._meta.model_name, '']
        extras = []

        for __, options in extra_urls.items():
            # isdetail, method_name, options = entry
            info[2] = options.method
            if options.details:
                extra_actions.append(options)
                uri = r'^%s/(?P<pk>.*)/$' % options.path
            else:
                uri = r'^%s/$' % options.path
                extra_actions.append(options)

            extras.append(re_path(uri, wrap(getattr(self, options.method)), name='{}_{}_{}'.format(*info)))

        for href in self.extra_buttons:
            extra_actions.append(href)
        self.extra_actions = sorted(extra_actions, key=lambda d: d.order)

        return extras + original
