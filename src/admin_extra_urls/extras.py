import inspect
from collections import namedtuple
from functools import update_wrapper

from django.conf import settings
from django.conf.urls import re_path
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.http import urlencode


def labelize(label):
    return label.replace('_', ' ').strip().title()


class ExtraUrlConfigException(RuntimeError):
    pass


IS_GRAPPELLI_INSTALLED = 'grappelli' in settings.INSTALLED_APPS

ExtraUrlConfig = namedtuple('ExtraUrlConfig', 'path,label,icon,perm,order,css_class,visible')
ExtraUrlOptions = namedtuple('ExtraUrlOptions',
                             'path,querystring,label,icon,perm,order,css_class,visible,authorized,method')

NOTSET = object()


def encapsulate(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def check_permission(permission, request, obj=None):
    if callable(permission):
        if not permission(request, obj):
            raise PermissionDenied
    elif not request.user.has_perm(permission):
        raise PermissionDenied
    return True


def link(path=None, label=None, icon='', permission=None,
         css_class="btn btn-success", order=999, visible=True, **kwargs):
    """
    decorator to mark ModelAdmin method as 'url' links.

    Each decorated method will be added to the ModelAdmin.urls and
    appear as button close to the 'Add <model>'.


    :param path: The name to use.
    :type path: str.

    - *path*:
        suffix to use to build url. Default: method name
    - **label**:
        label to display. Default: cleanded/titled version of method name
    - icon
        Fontawesome style icon.
        If set ``<i class="{{ options.icon }}"></i>`` will be prepend to the button label

    - css_class:
        CSS class to set. Default: "btn btn-success"
    - permission:

    - order:

    - visible:

    """

    if callable(permission):
        permission = encapsulate(permission)

    def link_decorator(func):
        args = inspect.getfullargspec(func).args
        if len(args) < 2:  # pragma: no cover
            raise ValueError('AdminExtraUrls: error decorating `{0}`. '
                             'Link methods need at least 2 arguments '
                             '(ie. action(self,request,*args, **kwargs)'.format(func.__name__))

        def _inner(self, request, *args, **kwargs):
            if permission:
                check_permission(permission, request)
            ret = func(self, request, *args, **kwargs)
            if not isinstance(ret, HttpResponse):
                url = reverse(admin_urlname(self.model._meta, 'changelist'))
                filters = request.GET.get('_changelist_filters', '')
                return HttpResponseRedirect("?".join([url, filters]))
            return ret

        _inner.func = func
        _inner.link = ExtraUrlConfig(path=path or func.__name__,
                                     label=label or labelize(func.__name__),
                                     icon=icon,
                                     perm=permission,
                                     order=order,
                                     css_class=css_class,
                                     visible=visible)

        return _inner

    return link_decorator


def action(path=None, label=None, icon='', permission=None,
           css_class="btn btn-success", order=999, visible=lambda o: o and o.pk,
           **kwargs):
    """
    decorator to mark ModelAdmin method as 'url' action.

    Each decorated method will be added to the ModelAdmin.urls and
    appear as button into the edit page

    :param path url path for the action
    :param label button label
    :param icon button icon
    :param required permission to run the action

    """

    if callable(permission):
        permission = encapsulate(permission)

    def action_decorator(func):
        args = inspect.getfullargspec(func).args
        if len(args) < 3:  # pragma: no cover
            raise ValueError('AdminExtraUrls: error decorating `{0}`. '
                             'Action methods need at least 3 arguments '
                             '(ie. action(self,request,id,*args, **kwargs)'.format(func.__name__))

        def _inner(modeladmin, request, pk, *args, **kwargs):
            if permission:
                obj = modeladmin.model.objects.get(pk=pk)
                check_permission(permission, request, obj)

            ret = func(modeladmin, request, pk, *args, **kwargs)

            if not isinstance(ret, HttpResponse):
                url = reverse(admin_urlname(modeladmin.model._meta, 'change'),
                              args=[pk])
                preserved_filters = request.GET.get('_changelist_filters', '')
                filters = urlencode({'_changelist_filters': preserved_filters})
                return HttpResponseRedirect("?".join([url, filters]))
            return ret

        _inner.action = ExtraUrlConfig(path or func.__name__,
                                       label or labelize(func.__name__),
                                       icon,
                                       permission,
                                       order,
                                       css_class,
                                       visible=visible)

        return _inner

    return action_decorator


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

    def __init__(self, model, admin_site):
        self.extra_buttons = []
        self.extra_detail_buttons = []
        super().__init__(model, admin_site)

    def get_urls(self):
        extra_buttons = []
        extra_detail_buttons = []
        extra_urls = {}
        for c in inspect.getmro(self.__class__):
            for method_name, method in c.__dict__.items():
                if hasattr(method, 'link'):
                    extra_urls[method_name] = (False, method_name,
                                               getattr(method, 'link'))
                elif hasattr(method, 'action'):
                    extra_urls[method_name] = (True, method_name,
                                               getattr(method, 'action'))

        original = super().get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            return update_wrapper(wrapper, view)

        info = [self.model._meta.app_label, self.model._meta.model_name, '']
        extras = []

        for __, entry in extra_urls.items():
            isdetail, method_name, options = entry
            info[2] = method_name
            if isdetail:
                extra_detail_buttons.append([method_name, options])
                uri = r'^%s/(?P<pk>.*)/$' % options.path
            else:
                uri = r'^%s/$' % options.path
                extra_buttons.append([method_name, options])

            extras.append(re_path(uri,
                                  wrap(getattr(self, method_name)),
                                  name='{}_{}_{}'.format(*info)))
        self.extra_buttons = sorted(extra_buttons, key=lambda d: d[-1].order)
        self.extra_detail_buttons = sorted(extra_detail_buttons, key=lambda d: d[-1].order)

        return extras + original
