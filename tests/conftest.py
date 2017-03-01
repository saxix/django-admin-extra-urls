import django_webtest
import pytest

from demo.models import DemoModel2


@pytest.fixture(scope='function')
def app(request):
    wtm = django_webtest.WebTestMixin()
    wtm.csrf_checks = False
    wtm._patch_settings()
    request.addfinalizer(wtm._unpatch_settings)
    return django_webtest.DjangoTestApp()


@pytest.fixture
def demomodel2():
    return DemoModel2.objects.get_or_create(name='name1')[0]

