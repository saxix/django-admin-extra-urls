# -*- coding: utf-8 -*-
import logging
from django.core.urlresolvers import reverse
from django.utils.translation import gettext as _
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


def test_link(app, admin_user):
    url = reverse('admin:demo_demomodel1_changelist')
    res = app.get(url, user=admin_user)
    res = res.click('Refresh').follow()
    assert map(str, res.context['messages']) == ['refresh called']


def test_link_reverse(app, admin_user):
    url = reverse('admin:demo_demomodel1_refresh')
    res = app.get(url, user=admin_user).follow()
    assert map(str, res.context['messages']) == ['refresh called']


def test_link_custom_path_reverse(app, admin_user):
    url = reverse('admin:demo_demomodel1_custom_path')
    assert url == '/admin/demo/demomodel1/a/b/'


@pytest.mark.django_db
def test_action(app, demomodel2, admin_user):
    url = reverse('admin:demo_demomodel2_change', args=[demomodel2.pk])
    res = app.get(url, user=admin_user)
    res = res.click(' Update').follow()
    assert map(str, res.context['messages']) == ['action called']


def test_default_httpresponseaction(app,  admin_user):
    url = reverse('admin:demo_demomodel1_changelist')
    res = app.get(url, user=admin_user)
    res = res.click('No_Response').follow()
    assert map(str, res.context['messages']) == ['No_response']
