from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from admin_extra_urls.extras import ExtraUrlMixin, link, action
from .models import DemoModel1, DemoModel2, DemoModel3


class Admin1(ExtraUrlMixin, admin.ModelAdmin):
    @link(label='Refresh')
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


admin.site.register(DemoModel1, Admin1)
admin.site.register(DemoModel2, Admin2)
admin.site.register(DemoModel3, Admin3)
