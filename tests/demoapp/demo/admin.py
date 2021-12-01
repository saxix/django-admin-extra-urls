from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.http import HttpResponseRedirect
from django.urls import reverse

from admin_extra_urls.api import url
from admin_extra_urls.api import confirm_action, ExtraUrlMixin, UrlButton
from admin_extra_urls.decorators import button

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

    @url(permission='demo.add_demomodel1', button=True)
    def refresh(self, request):
        opts = self.model._meta
        self.message_user(request, 'refresh called')
        return HttpResponseRedirect(reverse(admin_urlname(opts, 'changelist')))

    @url(button=UrlButton(label='Refresh'), permission=lambda request, object: False)
    def refresh_callable(self, request):
        opts = self.model._meta
        self.message_user(request, 'refresh called')
        return HttpResponseRedirect(reverse(admin_urlname(opts, 'changelist')))

    @button(path='a/b/', button=True)
    def custom_path(self, request):
        opts = self.model._meta
        self.message_user(request, 'refresh called')
        return HttpResponseRedirect(reverse(admin_urlname(opts, 'changelist')))

    @url(button=True)
    def no_response(self, request):
        self.message_user(request, 'No_response')

    @url(button=True)
    def confirm(self, request):
        def _action(request):
            pass

        return confirm_action(self, request, _action, "Confirm action",
                              "Successfully executed", )


class Admin2(ExtraUrlMixin, admin.ModelAdmin):
    list_filter = [TestFilter]

    @url(permission='demo_delete_demomodel2', button=True, details=True)
    def update(self, request, pk):
        opts = self.model._meta
        self.message_user(request, 'action called')
        return HttpResponseRedirect(reverse(admin_urlname(opts, 'changelist')))

    @url(button=True)
    def no_response(self, request, object_id):
        self.message_user(request, 'No_response')

    @url(permission=lambda request, obj: False)
    def update_callable_permission(self, request, object_id):
        opts = self.model._meta
        self.message_user(request, 'action called')
        return HttpResponseRedirect(reverse(admin_urlname(opts, 'changelist')))

    @url(path='a/b/<path:object_id>', button=True)
    def custom_update(self, request, object_id):
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
