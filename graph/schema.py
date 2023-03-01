import graphene
from .queries import EmployeeQuery, EmployeeMutation

class RootQuery(EmployeeQuery, graphene.ObjectType):
	pass


schema = graphene.Schema(query=RootQuery)