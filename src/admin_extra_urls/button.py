import logging
from inspect import getfullargspec

from django.urls import NoReverseMatch, reverse

from admin_extra_urls.utils import check_permission, get_preserved_filters, labelize

logger = logging.getLogger(__name__)


class UrlHandler:
    def __init__(self):
        pass


class BaseExtraButton:
    default_css_class = 'btn disable-on-click auto-disable'

    def __init__(self, **options):
        self.options = options
        # self.options.setdefault('html_attrs', {})
        # self.options.setdefault('display', lambda context: True)
        self.options.setdefault('icon', None)
        self.options.setdefault('change_list', False)
        self.options.setdefault('change_form', False)
        self.options.setdefault('url_name', None)
        self.options.setdefault('permission', None)
        self.options.setdefault('url', None)
        # self.options.setdefault('label', self.options['url'])
        # self.options.setdefault('name', None)
        self.options.setdefault('visible', True)
        # self.order = order
        # if display := options.get('display', empty) != empty:
        # self.display = (lambda context: True) if options.get('display') is None else options.get('display')
        # self.change_form = change_form
        # self.change_list = change_list
        # self.url_name = url_name
        # self._url = url
        self.context = None
        self.html_attrs = self.options.get('html_attrs', {})

    def __repr__(self):
        return f'<ExtraButton {self.options}>'

    def __html__(self):
        return f'[ExtraButton {self.options}]'

    def __copy__(self):
        return type(self)(**self.options)

    def __getattr__(self, item):
        if item in self.options:
            return self.options.get(item)
        raise ValueError(f'{item} is not a valid attribute for {self}')

    def visible(self):
        # if self.details and not self.original:
        #     return False
        f = self.options['visible']
        if callable(f):
            info = getfullargspec(f)
            params = []
            # BACKWARD COMPATIBLE CODE: To remove in future release
            if len(info.args) == 1:
                params = [self.context]
            elif len(info.args) == 2:
                params = [self.context.get('original', None),
                          self.context.get('request', None)]
            elif len(info.args) == 3:
                params = [self.context,
                          self.context.get('original', None),
                          self.context.get('request', None)]
            return f(*params)
        return f

    def authorized(self):
        if self.permission:
            return check_permission(self.permission, self.request, self.original)
        return True

    @property
    def request(self):
        if not self.context:
            raise ValueError(f"You need to call bind() to access 'request' on {self}")
        return self.context['request']

    @property
    def original(self):
        if not self.context:
            raise ValueError(f"You need to call bind() to access 'original' on {self}")
        return self.context.get('original', None)

    def bind(self, context):
        self.context = context
        # this is only for backward compatibility
        if self.name and 'id' not in self.html_attrs:
            self.html_attrs['id'] = f'btn-{self.name}'
        return self


class UrlButton(BaseExtraButton):
    def __init__(self, **options):
        super().__init__(**options)

    def label(self):
        return self.options.get('label', labelize(self.options.get('name', '')))

    @property
    def url(self):
        if self.options.get('url'):
            return self.options.get('url')
        try:
            if self.original:
                url = reverse(f'admin:{self.url_name}', args=[self.original.pk])
            else:
                url = reverse(f'admin:{self.url_name}')
            filters = get_preserved_filters(self.request)
            return f'{url}?{filters}'
        except NoReverseMatch as e:
            logger.exception(e)
            return f'javascript:alert("{e}")'


class Button(BaseExtraButton):
    def __init__(self, **options):
        super().__init__(**options)
        self._params = {}

    def label(self):
        return self.options.get('label', str(self.url))

    @property
    def url(self):
        if isinstance(self._params, dict):
            return self.options.get('url').format(**self._params)
        else:
            return self._params

    def bind(self, context):
        self.context = context
        if 'func' in self.options:
            self._params = (self.func(self) or {})
