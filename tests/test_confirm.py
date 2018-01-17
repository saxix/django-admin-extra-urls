# -*- coding: utf-8 -*-
import logging
from admin_extra_urls.extras import reverse

logger = logging.getLogger(__name__)


def test_confirm(django_app, admin_user):
    url = reverse('admin:demo_demomodel1_changelist')
    res = django_app.get(url, user=admin_user)
    res = res.click('Confirm')
    assert str(res.content).find("Confirm action")
    res = res.form.submit().follow()
    assert str(res.context['messages']._loaded_messages[0].message) == 'Successfully executed'
