.. _index:

=======================
Django Admin Extra-urls
=======================


Django application that offers one single mixin class ``ExtraUrlMixin``
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

    from admin_extra_urls.extras import ExtraUrlMixin, link, action

    class MyModelModelAdmin(ExtraUrlMixin, admin.ModelAdmin):

        @link() # /admin/myapp/mymodel/update_all/
        def update_all(self, request):
            ...
            ...


        @action() # /admin/myapp/mymodel/update/10/
        def update(self, request, pk):
            obj = self.get_object(pk=pk)
            ...


.. toctree::
    :maxdepth: 1

    api
    howto
    changes

