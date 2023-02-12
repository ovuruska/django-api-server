from django.core.paginator import Paginator


def pagination(self, queryset):
    """
        It returns a list that contains objects.
        Best way to use the function is to put it after all other filtering operations
    """
    page_start = self.request.query_params.get('page_start', None)
    page_length = self.request.query_params.get('page_length', None)
    if page_start and page_length:
        queryset = queryset[int(page_start):int(page_start) + int(page_length)]


    return queryset