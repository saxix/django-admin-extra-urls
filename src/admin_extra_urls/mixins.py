# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
from django.contrib import messages

from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

logger = logging.getLogger(__name__)


def _confirm_action(modeladmin, request,
                    action, message,
                    success_message="",
                    description='',
                    pk=None,
                    extra_context=None, **kwargs):
    opts = modeladmin.model._meta
    context = dict(
        modeladmin.admin_site.each_context(request),
        opts=opts,
        app_label=opts.app_label,
        message=message,
        description=description,
        **kwargs)
    if extra_context:
        context.update(extra_context)

    if request.method == 'POST':
        ret = action(request)
        modeladmin.message_user(request, success_message, messages.SUCCESS)
        return ret or HttpResponseRedirect(reverse(admin_urlname(opts,
                                                                 'changelist')))

    return TemplateResponse(request,
                            'admin_extra_urls/confirm.html',
                            context)

# class ConfirmActionMixin(object):
#     def _confirm(self, request, action, message, description='', info='', **kwargs):
#         return _confirm_action(self, request, action, message, description, info, **kwargs)
