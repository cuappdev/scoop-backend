from django.shortcuts import get_object_or_404


class MultipleFieldLookupMixin:
    """
    Mixin for multiple field filtering of URL parameters instead of the default single
    field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()                # Get the base queryset
        queryset = self.filter_queryset(queryset)     # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field):                # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)   # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj