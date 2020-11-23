.. _howto:

=====
HowTo
=====

Integrate with `django-import-export`
-------------------------------------
Import-export uses request to filter queryset,
but extra-urls save all filters in single query parameter ``_changelist_filters``
when building @link href.

::

    from django.http.request import QueryDict

    @link(label='Export')
    def _export(self, request):
        if '_changelist_filters' in request.GET:
            real_query = QueryDict(request.GET.get('_changelist_filters'))
            request.GET = real_query
        return self.export_action(request)

Credits to `@dglinyanov https://github.com/dglinyanov
