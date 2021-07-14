django-admin-extra-urls
=======================

.. image:: https://raw.githubusercontent.com/saxix/django-admin-extra-urls/develop/docs/image.png
    :scale: 80%
    :align: center


Pluggable django application that offers one single mixin class ``ExtraUrlMixin``
to easily add new url (and related buttons on the screen) to any ModelAdmin.

- ``button()`` decorator will produce a button in the list and change form views.
- ``href()`` to add button that point to external urls.



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

    from admin_extra_urls import api as extras

    class MyModelModelAdmin(extras.ExtraUrlMixin, admin.ModelAdmin):

        @extras.href(label='Search On Google', 'http://www.google.com?q={target}') # /admin/myapp/mymodel/update_all/
        def search_on_google(self, button):
            # this is called by the template engine just before rendering the button
            # `context` is the Context instance in the template
            if 'original' in button.context:
                obj = button.context['original']
                return {'target': obj.name}
            else:
                button.visible = False

        @extras.href()
        def search_on_bing(self, button):
            return 'http://www.bing.com?q=target'


        @extras.button() # /admin/myapp/mymodel/update_all/
        def consolidate(self, request):
            ...
            ...

        @extras.button() # /admin/myapp/mymodel/update/10/
        def update(self, request, pk):
            # if we use `pk` in the args, the button will be in change_form
            obj = self.get_object(request, pk)
            ...

        @button(urls=[r'^aaa/(?P<pk>.*)/(?P<state>.*)/$',
                      r'^bbb/(?P<pk>.*)/$'])
        def revert(self, request, pk, state=None):
            obj = self.get_object(request, pk)
            ...


        @extras.button(label='Truncate', permission=lambda request, obj: request.user.is_superuser)
        def truncate(self, request):

            if request.method == 'POST':
                self.model.objects._truncate()
            else:
                return extras._confirm_action(self, request, self.truncate,
                                       'Continuing will erase the entire content of the table.',
                                       'Successfully executed', )



If the return value from a `button` decorated method is a HttpResponse, that will be used.  Otherwise if the method contains the `pk`
argument user will be redirected to the 'update' view, otherwise and the browser will be redirected to the admin's list view


``button()`` options
--------------------

These are the arguments that ``button()`` accepts

+-------------+----------------------+----------------------------------------------------------------------------------------+
| path        | None                 | `path` url path for the button. Will be the url where the button will point to.        |
+-------------+----------------------+----------------------------------------------------------------------------------------+
| label       | None                 | Label for the button. By default the "labelized" function name.                        |
+-------------+----------------------+----------------------------------------------------------------------------------------+
| icon        |  ''                  | Icon for the button.                                                                   |
+-------------+----------------------+----------------------------------------------------------------------------------------+
| permission  | None                 | Permission required to use the button. Can be a callable (current object as argument). |
+-------------+----------------------+----------------------------------------------------------------------------------------+
| css_class   | "btn btn-success"    | Extra css classes to use for the button                                                |
+-------------+----------------------+----------------------------------------------------------------------------------------+
| order       | 999                  | In case of multiple button the order to use                                            |
+-------------+----------------------+----------------------------------------------------------------------------------------+
| visible     | lambda o: o and o.pk | callable or bool. By default do not display "action" button if in `add` mode           |
+-------------+----------------------+----------------------------------------------------------------------------------------+
| urls        | None                 | list of urls to be linked to the action.                                               |
+-------------+----------------------+----------------------------------------------------------------------------------------+



Integration with other libraries
--------------------------------

django-import-export
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    @admin.register(Rule)
    class RuleAdmin(ExtraUrlMixin, ImportExportMixin, BaseModelAdmin):
        @button(label='Export')
        def _export(self, request):
            if '_changelist_filters' in request.GET:
                real_query = QueryDict(request.GET.get('_changelist_filters'))
                request.GET = real_query
            return self.export_action(request)

        @button(label='Import')
        def _import(self, request):
            return self.import_action(request)


Running project tests locally
-----------------------------

Install the dev dependencies with ``pip install -e '.[dev]'`` and then run tox.

Links
-----

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


.. |master-build| image:: https://github.com/saxix/django-admin-extra-urls/actions/workflows/test.yml/badge.svg?branch=master
                    :target: https://github.com/saxix/django-admin-extra-urls

.. |master-cov| image:: https://codecov.io/gh/saxix/django-admin-extra-urls/branch/master/graph/badge.svg
                    :target: https://codecov.io/gh/saxix/django-admin-extra-urls

.. |dev-build| image:: https://github.com/saxix/django-admin-extra-urls/actions/workflows/test.yml/badge.svg?branch=develop
                  :target: https://github.com/saxix/django-admin-extra-urls

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
