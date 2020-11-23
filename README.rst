django-admin-extra-urls
=======================


pluggable django application that offers one single mixin class ``ExtraUrlMixin``
to easily add new url (and related buttons on the screen) to any ModelAdmin.


- ``action()`` decorator It will produce a button in the change form view.
- ``ButtonLink()`` to add button that pont to external urls.



Install
-------

.. code-block:: python

    pip install django-admin-extra-urls


After installation add it to ``INSTALLED_APPS``

.. code-block:: python


   INSTALLED_APPS = (
       ...
       'admin_extra_urls',
   )

How to use it
-------------

.. code-block:: python

    from admin_extra_urls import extras

    class MyModelModelAdmin(extras.ExtraUrlMixin, admin.ModelAdmin):
        extra_buttons = [extras.ButtonLink('/')]
        actions = ['smart_action']

        @extras.action() # /admin/myapp/mymodel/update_all/
        def update_all(self, request):
            ...
            ...

        @extras.action() # /admin/myapp/mymodel/update/10/
        def update(self, request, pk):
            # if `pk` exists the button will be in change_form
            obj = self.get_object(pk=pk)
            ...

        @extras.action() # /admin/myapp/mymodel/
        @extras.try_catch
        def smart_action(self, request, queryset=None):
            # apply actionnto the whole data without
            # check all
            if not queryset:
                queryset = self.model.objects.all()
            ...

        @extras.action(label='Truncate', permission=lambda request, obj: request.user.is_superuser)
        def truncate(self, request):

            if request.method == 'POST':
                self.model.objects._truncate()
            else:
                return extras._confirm_action(self, request, self.truncate,
                                       'Continuing will erase the entire content of the table.',
                                       'Successfully executed', )

You don't need to return a HttpResponse. The default behavior is:

    - if the  method contains the `pk` argument  button will be  displayed in the 'update' view and the browser will be redirected to ``change_view``


action() options
-------------------------

+------------+----------------------+----------------------------------------------------------------------------------------+
| path       | None                 | path url path for the action. will be the url where the button will point to.          |
+------------+----------------------+----------------------------------------------------------------------------------------+
| label      | None                 | label for the button. by default the "labelized" function name                         |
+------------+----------------------+----------------------------------------------------------------------------------------+
| icon       | ''                   | icon for the button                                                                    |
+------------+----------------------+----------------------------------------------------------------------------------------+
| permission | None                 | permission required to use the button. Can be a callable (current object as argument). |
+------------+----------------------+----------------------------------------------------------------------------------------+
| css_class  | "btn btn-success"    | extra css classes to use for the button                                                |
+------------+----------------------+----------------------------------------------------------------------------------------+
| order      | 999                  | in case of multiple button the order to use                                            |
+------------+----------------------+----------------------------------------------------------------------------------------+
| visible    | lambda o: o and o.pk | callable or bool. By default do not display "action" button if in `add` mode           |
+------------+----------------------+----------------------------------------------------------------------------------------+



Integration with other libraries
--------------------------------

django-import-export
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    @admin.register(Rule)
    class RuleAdmin(ExtraUrlMixin, ImportExportMixin, BaseModelAdmin):
        @action(label='Export')
        def _export(self, request):
            if '_changelist_filters' in request.GET:
                real_query = QueryDict(request.GET.get('_changelist_filters'))
                request.GET = real_query
            return self.export_action(request)

        @action(label='Import')
        def _import(self, request):
            return self.import_action(request)


Links
~~~~~

+--------------------+----------------+--------------+-----------------------------+
| Stable             | |master-build| | |master-cov| |                             |
+--------------------+----------------+--------------+-----------------------------+
| Development        | |dev-build|    | |dev-cov|    |                             |
+--------------------+----------------+--------------+-----------------------------+
| Project home page: |https://github.com/saxix/django-admin-extra-urls             |
+--------------------+---------------+---------------------------------------------+
| Issue tracker:     |https://github.com/saxix/django-admin-extra-urls/issues?sort |
+--------------------+---------------+---------------------------------------------+
| Download:          |http://pypi.python.org/pypi/admin-extra-urls/                |
+--------------------+---------------+---------------------------------------------+


.. |master-build| image:: https://secure.travis-ci.org/saxix/django-admin-extra-urls.png?branch=master
                    :target: http://travis-ci.org/saxix/django-admin-extra-urls/

.. |master-cov| image:: https://codecov.io/gh/saxix/django-admin-extra-urls/branch/master/graph/badge.svg
                    :target: https://codecov.io/gh/saxix/django-admin-extra-urls

.. |dev-build| image:: https://secure.travis-ci.org/saxix/django-admin-extra-urls.png?branch=develop
                  :target: http://travis-ci.org/saxix/django-admin-extra-urls/

.. |dev-cov| image:: https://codecov.io/gh/saxix/django-admin-extra-urls/branch/develop/graph/badge.svg
                    :target: https://codecov.io/gh/saxix/django-admin-extra-urls


.. |python| image:: https://img.shields.io/pypi/pyversions/admin-extra-urls.svg
    :target: https://pypi.python.org/pypi/admin-extra-urls/
    :alt: Supported Python versions

.. |pypi| image:: https://img.shields.io/pypi/v/admin-extra-urls.svg?label=version
    :target: https://pypi.python.org/pypi/admin-extra-urls/
    :alt: Latest Version

.. |license| image:: https://img.shields.io/pypi/l/admin-extra-urls.svg
    :target: https://pypi.python.org/pypi/admin-extra-urls/
    :alt: License

.. |travis| image:: https://travis-ci.org/saxix/django-admin-extra-urls.svg?branch=develop
    :target: https://travis-ci.org/saxix/django-admin-extra-urls

.. |django| image:: https://img.shields.io/badge/Django-1.8-orange.svg
    :target: http://djangoproject.com/
    :alt: Django 1.7, 1.8
