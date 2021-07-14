import inspect
from enum import unique, IntEnum
from functools import wraps

from django.contrib import messages
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.http import urlencode

from .config import ButtonAction, ButtonHREF, empty
from .utils import check_permission, deprecated, encapsulate, labelize, Display


def try_catch(f):
    @wraps(f)
    def _inner(modeladmin, request, *args, **kwargs):
        try:
            ret = f(modeladmin, request, *args, **kwargs)
            modeladmin.message_user(request, 'Success', messages.SUCCESS)
            return ret
        except Exception as e:
            modeladmin.message_user(request, str(e), messages.ERROR)

    return _inner


def button(path=None, label=None, icon='', permission=None, visible=empty,
           css_class="btn-action auto-disable", order=999, urls=None,
           display=Display.NOT_SET, group=None):
    """
    decorator to mark ModelAdmin method.

    Each decorated method will be added to the ModelAdmin.urls and
    appear as button close to the 'Add <model>' button.

    :param path: url path
    :type path: str
    :param label: button label
    :type label: str
    :param icon: button icon.
    :type icon: str
    :param permission: required permission. Can be a callable
    :type permission: Any
    :param css_class: button css classes
    :type css_class: str
    :param order: button order
    :type order: int
    :param visible: button visibility. Can be a callable
    :type visible: Any
    :param display
    :param urls
    """

    if callable(permission):
        permission = encapsulate(permission)

    def action_decorator(func):
        sig = inspect.signature(func)
        # modeladmin = list(sig.parameters)[0]
        args = list(sig.parameters)[1:2]
        if not args == ['request']:
            raise ValueError('AdminExtraUrls: error decorating `{0}`. '
                             'action need 2 or 3 arguments '
                             '(ie. action(self, request, pk, *args, **kwargs)'.format(func.__name__))
        details = 'pk' in sig.parameters
        if not visible == empty:
            visibility = visible
        elif details:
            visibility = lambda o, r: o and details and o.pk
        else:
            visibility = bool(visible)

        # Backward comm
        if display == Display.NOT_SET:
            if details:
                _display = Display.CHANGE_FORM
            else:
                _display = Display.CHANGELIST
        else:
            _display = display

        def _inner(modeladmin, request, *args, **kwargs):
            if details:
                pk = kwargs['pk']
                obj = modeladmin.get_object(request, pk)
                url = reverse(admin_urlname(modeladmin.model._meta, 'change'),
                              args=[pk])
                if permission:
                    check_permission(permission, request, obj)

            else:
                url = reverse(admin_urlname(modeladmin.model._meta, 'changelist'))
                if permission:
                    check_permission(permission, request)
            ret = func(modeladmin, request, *args, **kwargs)

            if not isinstance(ret, HttpResponse):
                preserved_filters = request.GET.get('_changelist_filters', '')
                filters = urlencode({'_changelist_filters': preserved_filters})
                return HttpResponseRedirect("?".join([url, filters]))
            return ret

        _inner.action = ButtonAction(func=func,
                                     # modeladmin=modeladmin,
                                     path=path,
                                     label=label or labelize(func.__name__),
                                     icon=icon,
                                     display=_display,
                                     group=group,
                                     permission=permission,
                                     order=order,
                                     css_class=css_class,
                                     visible=visibility,
                                     urls=urls,
                                     details=details)

        return _inner

    return action_decorator


@deprecated(button, "{name}() decorator has been deprecated. Use {updated}() now")
def action(*a, **kw):
    return button(*a, **kw)


def href(*, label=None, url=None, icon='', permission=None, html_attrs=None,
         css_class="btn-href", order=999, visible=empty, display=Display.NOT_SET, details=True, group=None):
    """
    decorator to mark ModelAdmin method.

    Each decorated method will show a button in the changelist/change_form page

    :param label: button label. Normalized method name will be used ad default
    :type label: str
    :param url:
    :param icon: button icon.
    :type icon: str
    :param permission: required permission. Can be a callable
    :type permission: Any
    :param details: if True will be visible only in change_form, if `None`
    :param css_class: button css classes
    :type css_class: str
    :param order: button order
    :type order: int
    :param visible: button visibility. Can be a callable
    :type visible: Any
    :param html_attrs:
    """

    def action_decorator(func):
        def _inner(modeladmin, btn):
            return func(modeladmin, btn)

        _inner.button = ButtonHREF(func=func,
                                   css_class=css_class,
                                   permission=permission,
                                   details=details,
                                   visible=visible,
                                   display=display,
                                   group=group,
                                   path=url,
                                   html_attrs=html_attrs or {},
                                   icon=icon,
                                   label=label or labelize(func.__name__),
                                   order=order)

        return _inner

    return action_decorator
