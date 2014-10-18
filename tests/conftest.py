import os
import sys
# import warnings
#
# warnings.filterwarnings("ignore", category=DeprecationWarning)


def pytest_configure(config):
    sys.path.append(os.path.join(os.path.dirname(__file__), "tests"))
    # import demo.settings
    # from django.conf import settings
    # if not settings.configured:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'demo.settings'
    try:
        from django.apps import AppConfig  # noqa
        import django
        django.setup()
    except ImportError:
        pass

