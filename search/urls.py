from django.urls import path

from search.views.search_customer import SearchCustomerListView

urlpatterns = [
	path("customer",SearchCustomerListView.as_view(), name="search_customer"),
]