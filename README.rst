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
            opts = self.model._meta
            return HttpResponseRedirect(reverse(admin_urlname(opts, 'changelist')))


        @action() # /admin/myapp/mymodel/update/10/
        def update(self, request, pk):
            ...
            ...
            opts = self.model._meta
            return HttpResponseRedirect(reverse(admin_urlname(opts, 'change'), args=[pk]))
