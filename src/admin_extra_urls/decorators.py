import inspect

from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.http import urlencode

from .button import Button
from .config import UrlConfig
from .utils import check_permission, empty, encapsulate


def url(permission=None, button=False, details=empty, path=None, **extra):
    if callable(permission):
        permission = encapsulate(permission)

    def decorator(func):
        sig = inspect.signature(func)
        object_id_arg_name = 'pk'  # backward compatibility
        if len(sig.parameters) > 2:
            object_id_arg_name = list(sig.parameters)[2]
        if details == empty:
            _details = object_id_arg_name in sig.parameters
        else:
            _details = details

        url_config = UrlConfig(func=func,
                               permission=permission,
                               button=button,
                               details=_details,
                               path=path,
                               object_id_arg_name=object_id_arg_name,
                               **extra)

        def view(modeladmin, request, *args, **kwargs):
            if url_config.details:
                pk = kwargs[object_id_arg_name]
                obj = modeladmin.get_object(request, pk)
                url_path = reverse(admin_urlname(modeladmin.model._meta, 'change'),
                                   args=[pk])
                if url_config.permission:
                    check_permission(url_config.permission, request, obj)

            else:
                url_path = reverse(admin_urlname(modeladmin.model._meta, 'changelist'))
                if url_config.permission:
                    check_permission(url_config.permission, request)

            ret = func(modeladmin, request, *args, **kwargs)

            if not isinstance(ret, HttpResponse):
                preserved_filters = request.GET.get('_changelist_filters', '')
                filters = urlencode({'_changelist_filters': preserved_filters})
                return HttpResponseRedirect('?'.join([url_path, filters]))
            return ret

        view.url = url_config

        return view

    return decorator


def button(**kwargs):
    url_args = {'permission': kwargs.pop('permission', None),
                'details': kwargs.pop('details', empty),
                'path': kwargs.pop('path', None),
                }
    if urls := kwargs.pop('urls', None):
        if len(urls) > 1:
            raise ValueError('urls in not supported in this version of admin-extra-urls')
        url_args['path'] = urls[0]

    url_args['button'] = {'visible': kwargs.pop('visible', True)}
    if 'label' in kwargs:
        url_args['button']['label'] = kwargs.pop('label')
    return url(**url_args)


def link(**kwargs):
    url_args = {'permission': kwargs.pop('permission', None),
                'button': Button(html_attrs=kwargs.pop('html_attrs', {}),
                                 change_list=True,
                                 change_form=True,
                                 visible=True,
                                 url=kwargs.get('url', '.')
                                 ),
                'details': kwargs.pop('details', empty),
                'path': kwargs.pop('path', None)
                }
    if 'label' in kwargs:
        url_args['button'].options['label'] = kwargs.pop('label')

    return url(**url_args)


href = link
