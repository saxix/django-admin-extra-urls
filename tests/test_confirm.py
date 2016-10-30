# -*- coding: utf-8 -*-
import logging
from django.core.urlresolvers import reverse
from django_dynamic_fixture import G
import django_webtest
import pytest
from demo.models import DemoModel2

logger = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def app(request):
    wtm = django_webtest.WebTestMixin()
    wtm.csrf_checks = False
    wtm._patch_settings()
    request.addfinalizer(wtm._unpatch_settings)
    return django_webtest.DjangoTestApp()


@pytest.fixture
def demomodel2():
    return G(DemoModel2)


def test_confirm(app, admin_user):
    url = reverse('admin:demo_demomodel1_changelist')
    res = app.get(url, user=admin_user)
    res = res.click('Confirm')
    assert str(res.content).find("Confirm action")
    res = res.form.submit().follow()
    assert str(res.context['messages']._loaded_messages[0].message) == 'Successfully executed'
