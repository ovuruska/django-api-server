from graphene_django.views import GraphQLView

from graph.schema import EmployeeSchema


class EmployeeGraphQL(GraphQLView ):

	schema = EmployeeSchema
	graphiql = True

