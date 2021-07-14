.. _index:

=======================
Django Admin Extra-urls
=======================


Django application that offers one single mixin class ``ExtraUrlMixin``
to easily add new url (and related buttons on the screen) to any ModelAdmin.

It provides two decorators ``button()`` and ``href()``.

- ``button()`` decorator will produce a button in the list and change form views.

- ``href()`` to add button that point to external urls.


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

    from admin_extra_urls.api import href, button

    class MyModelModelAdmin(extras.ExtraUrlMixin, admin.ModelAdmin):

        @href(label='Search On Google', 'http://www.google.com?q={target}')
        def search_on_google(self, button):
            # this is called by the template engine just before rendering the button
            # `context` is the Context instance in the template
            if 'original' in button.context:
                obj = button.context['original']
                return {'target': obj.name}
            else:
                button.visible = False

        @href()
        def search_on_bing(self, button):
            return 'http://www.bing.com?q=target'


        @button() # /admin/myapp/mymodel/update_all/
        def consolidate(self, request):
            ...
            ...

        @button() # /admin/myapp/mymodel/update/10/
        def update(self, request, pk):
            # if we use `pk` in the args, the button will be in change_form
            obj = self.get_object(request, pk)
            ...

        @button(urls=[r'^aaa/(?P<pk>.*)/(?P<state>.*)/$',
                      r'^bbb/(?P<pk>.*)/$'])
        def revert(self, request, pk, state=None):
            obj = self.get_object(request, pk)
            ...

        @button(label='Truncate', permission=lambda request, obj: request.user.is_superuser)
        def truncate(self, request):

            if request.method == 'POST':
                self.model.objects._truncate()
            else:
                return extras._confirm_action(self, request, self.truncate,
                                       'Continuing will erase the entire content of the table.',
                                       'Successfully executed', )



.. toctree::
    :maxdepth: 1

    api
    howto
    changes

