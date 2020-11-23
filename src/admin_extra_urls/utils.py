from django.core.exceptions import PermissionDenied


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
