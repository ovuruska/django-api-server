from django.db.models import Sum, Value, DateTimeField, IntegerField, F

from scheduling.models import Appointment


def get_payrolls(branch_id, start, end):
	"""
	:param branch_id: id of the branch
	:param start: start of the period
	:param end: end of the period
	:return: list of payrolls
	employee = EmployeeSerializer()
	branch = BranchSerializer()
	start = serializers.DateTimeField()
	end = serializers.DateTimeField()
	tips = serializers.DecimalField(max_digits=10, decimal_places=2)
	service_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
	product_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
	working_hours = serializers.IntegerField()

	class Meta:
		fields = "__all__"

	"""

	payrolls =  Appointment.objects.filter(branch=branch_id, start__gte=start, end__lte=end).values("employee__name").order_by("employee__name")\
		.annotate(
		employee_name=F("employee__name"),
		service_cost=Sum('cost'),
		product_cost=Sum('products__cost'),
		tips=Sum('tip'),
		working_hours=Value(0, output_field=IntegerField()),
		start=Value(start, output_field=DateTimeField()),
		end=Value(end, output_field=DateTimeField()))

	return payrolls