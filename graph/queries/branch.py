from django.apps import apps
import graphene
from graphene_django import DjangoObjectType

from graph.queries.employee import EmployeeType

Employee = apps.get_model('scheduling', 'Employee')
Branch = apps.get_model('scheduling', 'Branch')


class BranchType(DjangoObjectType):
	class Meta:
		model = Branch
		fields = '__all__'


class BranchQuery(graphene.ObjectType):
	get_branch = graphene.Field(BranchType, id=graphene.Int())
	branch_employees = graphene.List(EmployeeType,id=graphene.Int())

	def resolve_get_branch(self, info, id):
		return Branch.objects.get(id=id)

	def resolve_branch_employees(self, info, id):
		return Employee.objects.filter(branch=id)


class BranchMutation(graphene.ObjectType):
	pass
