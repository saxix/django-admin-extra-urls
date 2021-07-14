import inspect
import logging
from collections import namedtuple
from functools import partial, update_wrapper

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


class DummyAdminform:
    def __init__(self, **kwargs):
        self.prepopulated_fields = []
        self.__dict__.update(**kwargs)

    def __iter__(self):
        yield


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

    def get_common_context(self, request, pk=None, **kwargs):
        """ returns a general context that can be used in custom actions

        es.
        >>> from admin_extra_urls.api import ExtraUrlMixin, button
        >>> @button()
        ... def revert(self, request, pk):
        ...    context = self.get_common_context(request, pk, MONITORED_FIELDS=MONITORED_FIELDS)

        """
        opts = self.model._meta
        app_label = opts.app_label
        self.object = None

        context = {
            **self.admin_site.each_context(request),
            **kwargs,
            "opts": opts,
            "add": False,
            "change": True,
            "save_as": False,
            "has_delete_permission": self.has_delete_permission(request, pk),
            "has_editable_inline_admin_formsets": False,
            "has_view_permission": self.has_view_permission(request, pk),
            "has_change_permission": self.has_change_permission(request, pk),
            "has_add_permission": self.has_add_permission(request),
            "app_label": app_label,
            "adminform": DummyAdminform(model_admin=self),
        }
        context.setdefault("title", "")
        # context.update(**kwargs)
        if pk:
            self.object = self.get_object(request, pk)
            context["original"] = self.object
        return context

    def get_urls(self):
        extra_actions = []
        extra_buttons = []
        # extra_detail_actions = []
        extra_urls = {}
        for c in inspect.getmro(self.__class__):
            for method_name, method in c.__dict__.items():
                if callable(method):
                    if hasattr(method, 'action'):
                        extra_urls[method_name] = getattr(method, 'action')
                    elif hasattr(method, 'button'):
                        button = getattr(method, 'button')
                        button.func = partial(method, self)
                        button.func.__name__ = method_name
                        extra_buttons.append(button)

        original = super().get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            return update_wrapper(wrapper, view)

        info = [self.model._meta.app_label, self.model._meta.model_name, '']
        extras = []

        for __, options in extra_urls.items():
            info[2] = options.method
            if options.urls:
                for uri in options.urls:
                    options.details = 'pk' in uri
                    extras.append(re_path(uri,
                                          wrap(getattr(self, options.method)),
                                          name='{}_{}_{}'.format(*info)))
            else:
                if options.details:
                    extra_actions.append(options)
                    uri = r'^%s/(?P<pk>.*)/$' % options.path
                else:
                    uri = r'^%s/$' % options.path
                    extra_actions.append(options)
                extras.append(re_path(uri,
                                      wrap(getattr(self, options.method)),
                                      name='{}_{}_{}'.format(*info)))

        for href in extra_buttons:
            extra_actions.append(href)
        self.extra_actions = sorted(extra_actions, key=lambda d: d.order)

        return extras + original
