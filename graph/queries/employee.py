from django.apps import apps

import graphene
from graphene_django import DjangoObjectType

Employee = apps.get_model('scheduling', 'Employee')

class EmployeeType(DjangoObjectType):

	class Meta:
		model = Employee
		fields = '__all__'

class EmployeeQuery(graphene.ObjectType):
	employee = graphene.Field(EmployeeType, id=graphene.Int())

	def resolve_employee(self, info, id):
		return Employee.objects.get(id=id)

class EmployeeMutation(graphene.ObjectType):
	pass

