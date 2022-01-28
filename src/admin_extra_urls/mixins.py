import inspect
import logging
from functools import partial, update_wrapper

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.text import slugify

from admin_extra_urls.button import Button, UrlButton
from admin_extra_urls.checks import check_decorator_errors
from admin_extra_urls.utils import labelize

logger = logging.getLogger(__name__)

IS_GRAPPELLI_INSTALLED = 'grappelli' in settings.INSTALLED_APPS

NOTSET = object()


class ActionFailed(Exception):
    pass


def confirm_action(modeladmin, request,
                   action, message,
                   success_message='',
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


_confirm_action = confirm_action


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
    buttons = []

    def __init__(self, model, admin_site):
        self.extra_actions = []
        self.extra_buttons = []
        super().__init__(model, admin_site)

        for btn in self.buttons:
            self.extra_buttons.append(btn)

    def message_error_to_user(self, request, exception):
        self.message_user(request, f'{exception.__class__.__name__}: {exception}', messages.ERROR)

    @classmethod
    def check(cls, **kwargs):
        import sys
        errors = []
        # HACK: why django does not pass this flag?
        if '--deploy' in sys.argv:
            from django.core.checks import Error
            for btn in cls.buttons:
                if not isinstance(btn, Button):
                    errors.append(Error(f'{cls}.buttons can only contains "dict()" or '
                                        f'"admin_extra.url.api.Button" instances'))
            errors.extend(check_decorator_errors(cls))

        return errors

    def get_common_context(self, request, pk=None, **kwargs):
        opts = self.model._meta
        app_label = opts.app_label
        self.object = None

        context = {
            **self.admin_site.each_context(request),
            **kwargs,
            'opts': opts,
            'add': False,
            'change': True,
            'save_as': False,
            'has_delete_permission': self.has_delete_permission(request, pk),
            'has_editable_inline_admin_formsets': False,
            'has_view_permission': self.has_view_permission(request, pk),
            'has_change_permission': self.has_change_permission(request, pk),
            'has_add_permission': self.has_add_permission(request),
            'app_label': app_label,
            'adminform': DummyAdminform(model_admin=self),
        }
        context.setdefault('title', '')
        context.update(**kwargs)
        if pk:
            self.object = self.get_object(request, pk)
            context['original'] = self.object
        return context

    def get_urls(self):
        extra_urls = {}
        for cls in inspect.getmro(self.__class__):
            for method_name, method in cls.__dict__.items():
                if callable(method) and hasattr(method, 'url'):
                    extra_urls[method_name] = getattr(method, 'url')

        original = super().get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name
        extras = []

        for __, url_config in extra_urls.items():
            sig = inspect.signature(url_config.func)
            uri = ''
            if url_config.path:
                uri = url_config.path
            else:
                for arg in list(sig.parameters)[2:]:
                    uri += f'<path:{arg}>/'
                uri += f'{url_config.func.__name__}/'

            url_name = f'%s_%s_{url_config.func.__name__}' % info
            extras.append(path(uri,
                               wrap(getattr(self, url_config.func.__name__)),
                               name=url_name))

            if url_config.button:
                params = dict(label=labelize(url_config.func.__name__),
                              # func=url_config.func,
                              func=partial(url_config.func, self),
                              name=slugify(url_config.func.__name__),
                              details=url_config.details,
                              permission=url_config.permission,
                              change_form=url_config.details,
                              change_list=not url_config.details,
                              order=9999)

                if isinstance(url_config.button, Button):
                    params.update(url_config.button.options)
                    button = Button(**params)
                else:
                    if isinstance(url_config.button, UrlButton):
                        params.update(url_config.button.options)
                    elif isinstance(url_config.button, dict):
                        params.update(url_config.button)
                    elif bool(url_config.button):
                        pass
                    else:
                        raise ValueError(url_config.button)
                    params.update({'url_name': url_name})
                    button = UrlButton(**params)
                self.extra_buttons.append(button)

        return extras + original

    def get_changeform_buttons(self, request, original):
        return self.extra_buttons

    def get_changelist_buttons(self, request):
        return self.extra_buttons

    def get_action_buttons(self, request):
        return []
