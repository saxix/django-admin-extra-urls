import logging

from demo.models import DemoModel1
from django.contrib.admin import site
from django.urls import reverse

from admin_extra_urls.api import confirm_action

logger = logging.getLogger(__name__)


def test_confirm(django_app, admin_user):
    url = reverse('admin:demo_demomodel1_changelist')
    res = django_app.get(url, user=admin_user)
    res = res.click('Confirm')
    assert str(res.content).find("Confirm action")
    res = res.form.submit().follow()
    assert str(res.context['messages']._loaded_messages[0].message) == 'Successfully executed'


def test_confirm_action(rf, staff_user):
    request = rf.get('/customer/details')
    request.user = staff_user
    confirm_action(site._registry[DemoModel1], request,
                   lambda r: True,
                   "Confirm action",
                   "Successfully executed",
                   description="",
                   pk=None,
                   extra_context={'a': 1})
