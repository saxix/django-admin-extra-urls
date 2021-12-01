import ast
import inspect

from django.conf import settings
from django.core.checks import Warning


def get_all_permissions():
    from django.contrib.auth.models import Permission
    return [f'{p[0]}.{p[1]}'
            for p in (Permission.objects
                      .select_related('content_type')
                      .values_list('content_type__app_label', 'codename'))]


def check_decorator_errors(cls):
    target = cls
    standard_permissions = []
    errors = []
    if 'django.contrib.auth' in settings.INSTALLED_APPS:
        standard_permissions = get_all_permissions()

    def visit_FunctionDef(node):
        # deco = []
        for n in node.decorator_list:
            if isinstance(n, ast.Call):
                name = n.func.attr if isinstance(n.func, ast.Attribute) else n.func.id
            else:
                name = n.attr if isinstance(n, ast.Attribute) else n.id
            if name in ['href', ]:
                errors.append(Warning(f'"{cls.__name__}.{node.name}" uses deprecated decorator "@{name}"',
                                      id='admin_extra_urls.W001'))
            elif name in ['button']:
                if standard_permissions:
                    for k in n.keywords:
                        if k.arg == 'permission' and isinstance(k.value, ast.Constant):
                            perm_name = k.value.value
                            if perm_name not in standard_permissions:
                                errors.append(Warning(f'"{cls.__name__}.{node.name}" '
                                                      f'is checking for a non existent permission '
                                                      f'"{perm_name}"',
                                                      id='admin_extra_urls.PERM', ))

    node_iter = ast.NodeVisitor()
    node_iter.visit_FunctionDef = visit_FunctionDef
    node_iter.visit(ast.parse(inspect.getsource(target)))
    return errors
