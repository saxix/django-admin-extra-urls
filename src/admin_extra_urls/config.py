from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.urls import reverse

from admin_extra_urls.utils import get_preserved_filters, safe

empty = object()


class Button:
    def __init__(self, path, *, label=None, icon='', permission=None,
                 css_class="btn btn-success disable-on-click", order=999, visible=empty,
                 modeladmin=None,
                 details=True, urls=None):
        self.path = path
        self.label = label or path

        self.icon = icon
        self._perm = permission
        self.order = order
        self.css_class = css_class
        self._visible = visible
        self._bound = False
        self.details = details
        self.urls = urls
        self.modeladmin = modeladmin

    def bind(self, context):
        self.context = context
        obj = context.get('original', None)
        request = context['request']
        user = request.user
        self.querystring = get_preserved_filters(request)
        if callable(self._visible):
            self.visible = safe(self._visible, obj)
        else:
            self.visible = self._visible

        if self._perm is None:
            self.authorized = True
        elif callable(self._perm):
            self.authorized = self._perm(request, obj)
        else:
            self.authorized = user.has_perm(self._perm)


class ButtonHREF(Button):
    def __init__(self, func, *, path=None, label=None, icon='', permission=None,
                 css_class="btn btn-success", order=999, visible=empty,
                 modeladmin=None, details=True, html_attrs=None):
        self.func = func
        self.html_attrs = html_attrs
        self.callback_paramenter = None
        super().__init__(path=path, label=label, icon=icon, permission=permission,
                         css_class=css_class, order=order, visible=visible,
                         modeladmin=modeladmin, details=details)

    def __repr__(self):
        return f"<ButtonHREF {self.label} {self.func.__name__}>"

    def bind(self, context):
        super().bind(context)
        self.callback_paramenter = self.func(self)

    def url(self):
        if isinstance(self.callback_paramenter, dict):
            return self.path.format(**self.callback_paramenter)
        else:
            return self.callback_paramenter


class ButtonAction(Button):
    def __init__(self, func, **kwargs):
        self.func = func
        super().__init__(**kwargs)
        self.path = self.path or func.__name__
        self.method = func.__name__

    def url(self):
        opts = self.context['opts']
        if self.details:
            base_url = reverse(admin_urlname(opts, self.method),
                               args=[self.context['original'].pk])
        else:
            base_url = reverse(admin_urlname(opts, self.method))
        return "%s?%s" % (base_url, self.querystring)
