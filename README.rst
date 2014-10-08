admin-extra-urls
================

this plugable django application that offer one single Mixin ``ExtraUrlMixin``
to easily add new url (and related buttons on the screen) to any ModelAdmin.

Example::

    class MyModelModelAdmin(ExtraUrlMixin, admin.ModelAdmin):

        @link() # /admin/myapp/mymodel/update_all/
        def update_all(self, request):
            ...
            ...

        @action() # /admin/myapp/mymodel/update/10/
        def update(self, request):
            ...
            ...
