import os
import sys
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


def pytest_configure(config):
    from django.conf import settings
    sys.path.append(os.path.dirname(__file__))
    if not settings.configured:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'demo.settings'

    try:
        from django.apps import AppConfig  # noqa
        import django
        django.setup()
    except ImportError:
        pass

