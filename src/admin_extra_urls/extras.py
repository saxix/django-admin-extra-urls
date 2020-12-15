import warnings

from .api import *  # noqa: F401

warnings.warn("extras is deprecated. Please use `from admon_extra_urls import api`", DeprecationWarning)
