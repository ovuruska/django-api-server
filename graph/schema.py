import graphene
from .queries import EmployeeQuery, EmployeeMutation, BranchQuery, BranchMutation

# Insert the queries and mutations from the other files
class RootQuery(EmployeeQuery, BranchQuery, graphene.ObjectType):
	pass


class RootMutation(EmployeeMutation, BranchMutation, graphene.ObjectType):
	pass


EmployeeSchema = graphene.Schema(query=RootQuery)
