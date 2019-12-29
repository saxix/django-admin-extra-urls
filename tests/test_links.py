import logging

from django.contrib.auth.models import Permission

from admin_extra_urls.extras import reverse

logger = logging.getLogger(__name__)


def test_link(django_app, staff_user):
    perms = Permission.objects.filter(codename__in=['add_demomodel1', 'change_demomodel1'])
    staff_user.user_permissions.add(*perms)
    url = reverse('admin:demo_demomodel1_changelist')
    res = django_app.get(url, user=staff_user)
    res = res.click('Refresh').follow()
    assert str(res.context['messages']._loaded_messages[0].message) == 'refresh called'


def test_link_preserve_filters(django_app, staff_user):
    perms = Permission.objects.filter(codename__in=['add_demomodel1', 'change_demomodel1'])
    staff_user.user_permissions.add(*perms)
    base_url = reverse('admin:demo_demomodel1_changelist')
    url = "%s?filter=on" % base_url
    res = django_app.get(url, user=staff_user)
    link = res.pyquery('#btn-refresh')[0]
    assert link.get('href') == '/admin/demo/demomodel1/refresh/?_changelist_filters=filter%3Don'


def test_link_reverse(django_app, staff_user):
    perms = Permission.objects.filter(codename__in=['add_demomodel1', 'change_demomodel1'])
    staff_user.user_permissions.add(*perms)
    url = reverse('admin:demo_demomodel1_refresh')
    res = django_app.get(url, user=staff_user).follow()
    assert str(res.context['messages']._loaded_messages[0].message) == 'refresh called'


def test_link_custom_path_reverse(django_app, admin_user):
    url = reverse('admin:demo_demomodel1_custom_path')
    assert url == '/admin/demo/demomodel1/a/b/'


def test_default_httpresponseaction(app, admin_user):
    url = reverse('admin:demo_demomodel1_changelist')
    res = app.get(url, user=admin_user)
    res = res.click('No Response').follow()
    assert str(res.context['messages']._loaded_messages[0].message) == 'No_response'


def test_link_permission(app, staff_user):
    perms = Permission.objects.filter(codename__in=['change_demomodel1'])
    staff_user.user_permissions.add(*perms)

    url = reverse('admin:demo_demomodel1_changelist')
    res = app.get(url, user=staff_user)
    assert not res.pyquery('#btn-refresh')

    url = reverse('admin:demo_demomodel1_refresh')

    res = app.get(url, user=staff_user, expect_errors=True)
    assert res.status_code == 403


def test_link_permission_callable(app, staff_user):
    perms = Permission.objects.filter(codename__in=['change_demomodel1'])
    staff_user.user_permissions.add(*perms)

    url = reverse('admin:demo_demomodel1_changelist')
    res = app.get(url, user=staff_user)
    assert not res.pyquery('#btn-refresh-callable')

    url = reverse('admin:demo_demomodel1_refresh_callable')
    res = app.get(url, user=staff_user, expect_errors=True)
    assert res.status_code == 403
