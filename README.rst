admin-extra-urls
================


pluggable django application that offers one single mixin class ``ExtraUrlMixin``
to easily add new url (and related buttons on the screen) to any ModelAdmin.

It provides two decorators ``link()`` and ``action()``.

- ``link()`` is intended to be used for multiple records. It will produce a button in the change list view.

- ``action()`` works on a single record. It will produce a button in the change form view.



Install
-------

.. code-block:: python

    pip install admin-extra-urls


After installation add it to ``INSTALLED_APPS``

.. code-block:: python


   INSTALLED_APPS = (
       ...
       'admin_extra_urls',
   )

How to use it
-------------

.. code-block:: python

    class MyModelModelAdmin(ExtraUrlMixin, admin.ModelAdmin):

        @link() # /admin/myapp/mymodel/update_all/
        def update_all(self, request):
            ...
            ...


        @action() # /admin/myapp/mymodel/update/10/
        def update(self, request, pk):
            ...
            ...

You don't need to return a HttpResponse. The default behavior is:

    - with `link()` browser will be redirected to ``changelist_view``

    - with `action()` browser will be redirected to ``change_view``


More options
------------

.. code-block:: python


    @link(label='Update', icon="icon-refresh icon-white", permission='model_change", order=-1)
    def update_all(self, request):
            ....


*Note*

    The package contains a ``UploadMixin`` to manage custom file uploads
    (simply set `upload_handler` to a function.
    This can be checked to see how to create wizard with an intermediate form.


Links
~~~~~

+--------------------+----------------+--------------+-----------------------------+
| Stable             | |master-build| | |master-cov| | |master-req|                |
+--------------------+----------------+--------------+-----------------------------+
| Development        | |dev-build|    | |dev-cov|    | |dev-req|                   |
+--------------------+----------------+--------------+-----------------------------+
| Project home page: |https://github.com/saxix/django-admin-extra-urls             |
+--------------------+---------------+---------------------------------------------+
| Issue tracker:     |https://github.com/saxix/django-admin-extra-urls/issues?sort |
+--------------------+---------------+---------------------------------------------+
| Download:          |http://pypi.python.org/pypi/django-admin-extra-urls/         |
+--------------------+---------------+---------------------------------------------+


.. |master-build| image:: https://secure.travis-ci.org/saxix/django-admin-extra-urls.png?branch=master
                    :target: http://travis-ci.org/saxix/django-admin-extra-urls/

.. |master-cov| image:: https://coveralls.io/repos/saxix/django-admin-extra-urls/badge.png?branch=master
                    :target: https://coveralls.io/r/saxix/django-admin-extra-urls

.. |master-req| image:: https://requires.io/github/saxix/django-admin-extra-urls/requirements.png?branch=master
                    :target: https://requires.io/github/saxix/django-admin-extra-urls/requirements/?branch=master
                    :alt: Requirements Status


.. |dev-build| image:: https://secure.travis-ci.org/saxix/django-admin-extra-urls.png?branch=develop
                  :target: http://travis-ci.org/saxix/django-admin-extra-urls/

.. |dev-cov| image:: https://coveralls.io/repos/saxix/django-admin-extra-urls/badge.png?branch=develop
                :target: https://coveralls.io/r/saxix/django-admin-extra-urls

.. |dev-req| image:: https://requires.io/github/saxix/django-admin-extra-urls/requirements.png?branch=develop
                    :target: https://requires.io/github/saxix/django-admin-extra-urls/requirements/?branch=develop
                    :alt: Requirements Status


.. |python| image:: https://pypip.in/py_versions/django-admin-extra-urls/badge.svg
    :target: https://pypi.python.org/pypi/django-admin-extra-urls/
    :alt: Supported Python versions

.. |pypi| image:: https://pypip.in/version/admin-extra-urls/badge.svg?text=version
    :target: https://pypi.python.org/pypi/admin-extra-urls/
    :alt: Latest Version

.. |license| image:: https://pypip.in/license/admin-extra-urls/badge.svg
    :target: https://pypi.python.org/pypi/admin-extra-urls/
    :alt: License

.. image:: https://pypip.in/wheel/django-admin-extra-urls/badge.svg
    :target: https://pypi.python.org/pypi/django-admin-extra-urls/
    :alt: Wheel Status

.. |travis| image:: https://travis-ci.org/saxix/django-admin-extra-urls.svg?branch=develop
    :target: https://travis-ci.org/saxix/django-admin-extra-urls

.. |django| image:: https://img.shields.io/badge/Django-1.8-orange.svg
    :target: http://djangoproject.com/
    :alt: Django 1.7, 1.8
