from django.core.paginator import Paginator


def pagination(request, queryset):
    """
        It returns a list that contains objects.
        Best way to use the function is to put it after all other filtering operations
    """
    page_start = request.query_params.get('page_start', None)
    if page_start:
        page_length = request.query_params.get('page_length', None)
        if page_length:
            queryset = queryset[int(page_start):int(page_start) + int(page_length)]


    return queryset