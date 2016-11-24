# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from .extras import ExtraUrlMixin, link


class UploadMixin(ExtraUrlMixin):
    upload_handler = None
    upload_form_template = 'admin_extra_urls/upload.html'

    def get_upload_form_template(self, request):
        return self.upload_form_template

    @link(icon='icon-upload')
    def upload(self, request):
        opts = self.model._meta
        context = dict(
            self.admin_site.each_context(request),
            opts=opts,
            help_text=self.upload_handler.__doc__,
            app_label=opts.app_label,
        )
        if request.method == 'POST':
            if 'file' in request.FILES:
                try:
                    f = request.FILES['file']
                    rows, updated, created = self.upload_handler(f)
                    msg = "Loaded {}. Parsed:{} " \
                          "updated:{} created:{}".format(f.name,
                                                         rows,
                                                         updated,
                                                         created)
                    self.message_user(request, msg, messages.SUCCESS)
                    return HttpResponseRedirect(reverse(admin_urlname(opts,
                                                                      'changelist')))
                except Exception as e:
                    self.message_user(request, str(e), messages.ERROR)

        return TemplateResponse(request,
                                self.get_upload_form_template(request),
                                context)
