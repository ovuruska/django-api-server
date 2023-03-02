import graphene
from .queries import EmployeeQuery, EmployeeMutation, BranchQuery, BranchMutation


class RootQuery(EmployeeQuery, BranchQuery, graphene.ObjectType):
	pass


class RootMutation(EmployeeMutation, BranchMutation, graphene.ObjectType):
	pass


EmployeeSchema = graphene.Schema(query=RootQuery)
