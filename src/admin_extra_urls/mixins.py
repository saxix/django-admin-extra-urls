# -*- coding: utf-8 -*-
import logging

from django.contrib import messages
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from .extras import reverse

logger = logging.getLogger(__name__)


class ActionFailed(Exception):
    pass


def _confirm_action(modeladmin, request,
                    action, message,
                    success_message="",
                    description='',
                    pk=None,
                    extra_context=None,
                    template='admin_extra_urls/confirm.html',
                    error_message=None,
                    **kwargs):
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
        ret = None
        try:
            ret = action(request)
            modeladmin.message_user(request, success_message, messages.SUCCESS)
        except Exception as e:
            modeladmin.message_user(request, error_message or str(e), messages.ERROR)

        return ret or HttpResponseRedirect(reverse(admin_urlname(opts,
                                                                 'changelist')))

    return TemplateResponse(request,
                            template,
                            context)

# class ConfirmActionMixin(object):
#     def _confirm(self, request, action, message, description='', info='', **kwargs):
#         return _confirm_action(self, request, action, message, description, info, **kwargs)
