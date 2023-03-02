from django.urls import path

from django.conf import settings

from graph.views.employee import EmployeeGraphQL

urlpatterns = [
	#path("", EmployeeGraphQL.as_view(graphiql=settings.DEBUG)),
]
