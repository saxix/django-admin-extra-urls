admin-extra-urls
================

this plugable django application that offer one single Mixin ``ExtraUrlMixin``
to easily add new url (and related buttons on the screen) to any ModelAdmin.

Install::

    pip install admin-extra-urls

After installation add it to ``INSTALLED_APPS``::

   INSTALLED_APPS = (
       ...
       'admin_extra_urls',
   )

Example::

    class MyModelModelAdmin(ExtraUrlMixin, admin.ModelAdmin):

        @link() # /admin/myapp/mymodel/update_all/
        def update_all(self, request):
            ...
            ...


        @action() # /admin/myapp/mymodel/update/10/
        def update(self, request, pk):
            ...
            ...


    methods decorated with `@link()` will return to `changelist view ` if no
    HttpResponse are returned

    methods decorated with `@action()` will return to `change view ` if no
    HttpResponse are returned


*Note*

    The package contains a ``UploadMixin`` to manage custom file uploads
    (simply set `upload_handler` to a function.
    This can be checked to see how to create wizard with an intermediate form.
