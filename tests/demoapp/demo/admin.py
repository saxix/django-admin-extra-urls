from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from admin_extra_urls.extras import ExtraUrlMixin, link, action
from admin_extra_urls.mixins import _confirm_action
from admin_extra_urls.upload import UploadMixin
from .models import DemoModel1, DemoModel2, DemoModel3, DemoModel4


class Admin1(ExtraUrlMixin, admin.ModelAdmin):
    @link(label='Refresh', permission='demo.add_demomodel1')
    def refresh(self, request):
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
                               "Successfully executed")


class Admin2(ExtraUrlMixin, admin.ModelAdmin):
    @action()
    def update(self, request, pk):
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
    upload_handler = lambda *args: None


admin.site.register(DemoModel1, Admin1)
admin.site.register(DemoModel2, Admin2)
admin.site.register(DemoModel3, Admin3)
admin.site.register(DemoModel4, Admin4)
