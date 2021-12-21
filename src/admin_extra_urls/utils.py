import inspect
import warnings
from functools import wraps
from urllib.parse import urlencode

from django.contrib import messages
from django.core.exceptions import PermissionDenied

empty = object()


def safe(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception:
        return False


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


def get_preserved_filters(request, **extras):
    filters = request.GET.get('_changelist_filters', '')
    if filters:
        preserved_filters = request.GET.get('_changelist_filters')
    else:
        preserved_filters = request.GET.urlencode()

    if preserved_filters:
        return urlencode({'_changelist_filters': preserved_filters})
    return ''


def labelize(label):
    return label.replace('_', ' ').strip().title()


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


def deprecated(updated, message='{name}() has been deprecated. Use {updated}() now'):
    if inspect.isfunction(updated):
        def decorator(func1):
            @wraps(func1)
            def new_func1(*args, **kwargs):
                warnings.simplefilter('always', DeprecationWarning)
                warnings.warn(
                    message.format(name=func1.__name__, updated=updated.__name__),
                    category=DeprecationWarning,
                    stacklevel=2
                )
                warnings.simplefilter('default', DeprecationWarning)
                return func1(*args, **kwargs)

            return new_func1

        return decorator
    else:
        raise TypeError('deprecated() first parameter must be a ' % repr(type(updated)))
