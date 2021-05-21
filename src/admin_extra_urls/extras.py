import warnings

from .api import *  # noqa: F403, F401

warnings.warn("extras is deprecated. Please use `from admin_extra_urls import api`", DeprecationWarning)
