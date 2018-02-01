# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import inspect

import django
import six

DJANGO2 = django.VERSION[0] == 2
DJANGO1 = django.VERSION[0] == 1

if six.PY3:
    getfullargspec = inspect.getfullargspec
else:
    getfullargspec = inspect.getargspec

# MONITOR THIS: DJANGO version compatibility code:
if DJANGO2:
    from django.urls import reverse  # noqa
else:
    from django.core.urlresolvers import reverse  # noqa
