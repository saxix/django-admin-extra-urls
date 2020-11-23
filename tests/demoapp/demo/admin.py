from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.http import HttpResponseRedirect
from django.urls import reverse

from admin_extra_urls.decorators import link, action
from admin_extra_urls.mixins import _confirm_action, ExtraUrlMixin

from .models import DemoModel1, DemoModel2, DemoModel3, DemoModel4
from .upload import UploadMixin


class TestFilter(SimpleListFilter):
    parameter_name = 'filter'
    title = "Dummy filter for testing"

    def lookups(self, request, model_admin):
        return (
            ('on', "On"),
            ('off', "Off"),
        )

    def queryset(self, request, queryset):
        return queryset


class Admin1(ExtraUrlMixin, admin.ModelAdmin):
    list_filter = [TestFilter]

    @link(label='Refresh', permission='demo.add_demomodel1')
    def refresh(self, request):
        opts = self.model._meta
        self.message_user(request, 'refresh called')
        return HttpResponseRedirect(reverse(admin_urlname(opts, 'changelist')))

    @link(label='Refresh', permission=lambda request, object: False)
    def refresh_callable(self, request):
        opts = self.model._meta
        self.message_user(request, 'refresh called')
        return HttpResponseRedirect(reverse(admin_urlname(opts, 'changelist')))

    @link(path='a/b')
    def custom_path(self, request):
        opts = self.model._meta
        self.message_user(request, 'refresh called')
        return HttpResponseRedirect(reverse(admin_urlname(opts, 'changelist')))

    @link()
    def no_response(self, request):
        self.message_user(request, 'No_response')

    @link()
    def confirm(self, request):
        def _action(request):
            pass

        return _confirm_action(self, request, _action, "Confirm action",
                               "Successfully executed", )


class Admin2(ExtraUrlMixin, admin.ModelAdmin):
    list_filter = [TestFilter]

    @action(permission='demo_delete_demomodel2')
    def update(self, request, pk):
        opts = self.model._meta
        self.message_user(request, 'action called')
        return HttpResponseRedirect(reverse(admin_urlname(opts, 'changelist')))

    @action()
    def no_response(self, request, pk):
        self.message_user(request, 'No_response')

    @action(permission=lambda request, obj: False)
    def update_callable_permission(self, request, pk):
        opts = self.model._meta
        self.message_user(request, 'action called')
        return HttpResponseRedirect(reverse(admin_urlname(opts, 'changelist')))

    @action(path='a/b')
    def custom_update(self, request, pk):
        opts = self.model._meta
        self.message_user(request, 'action called')
        return HttpResponseRedirect(reverse(admin_urlname(opts, 'changelist')))


class Admin3(admin.ModelAdmin):
    pass


class Admin4(UploadMixin, admin.ModelAdmin):
    upload_handler = lambda *args: [1, 2, 3]


admin.site.register(DemoModel1, Admin1)
admin.site.register(DemoModel2, Admin2)
admin.site.register(DemoModel3, Admin3)
admin.site.register(DemoModel4, Admin4)
