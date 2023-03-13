from datetime import datetime

from django.apps import apps
from django.forms.models import model_to_dict
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response

from scheduling.models import EmployeeWorkingHour
from scheduling.selectors.working_hours import get_employee_working_hours,set_employee_working_hours
from scheduling.serializers.wh_employee import EmployeeWorkingHourSerializer, EmployeeWorkingHourRetrieveSerializer


class EmployeeWorkingHourRetrieveAPIView(generics.RetrieveAPIView):
    queryset = EmployeeWorkingHour.objects.all()
    serializer_class = EmployeeWorkingHourSerializer
    def get(self, request, *args, **kwargs):
        employee_id = kwargs.get("pk")
        start_date = request.query_params.get("start", None)
        end_date = request.query_params.get("end", None)
        queryset = EmployeeWorkingHour.objects.filter(employee_id=employee_id)

        if start_date is not None and end_date is not None:
            queryset = queryset.filter(start__gte=start_date, end__lte=end_date)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EmployeeWorkingHourCreateAPIView(generics.CreateAPIView):
    queryset = EmployeeWorkingHour.objects.all()
    serializer_class = EmployeeWorkingHourSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



"""class EmployeeWorkingHourRetrieveCreateView(generics.ListAPIView,generics.CreateAPIView):
    
    API endpoint that allows users to be viewed or edited.
    {
        "start": "2020-01-01",
        "end": "2020-01-31",
        "employee":Employee
        "Branch":Branch
    }

    
    Employee = apps.get_model(
        'scheduling',
        'Employee'
    )
    queryset = EmployeeWorkingHour.objects.all()
    serializer_class = EmployeeWorkingHourSerializer(many=True)

    def post(self, request, *args, **kwargs):
        employee_id = self.kwargs.get("pk", None)
        data = request.data
        if type(data) != list:
            data = [data]
        results = []
        for item in data:

            result = set_employee_working_hours(employee_id,
                                                   item["start"], item["end"],item["branch"])
            results.append(result)
        return Response(data=results, status=200)

    def get(self, request, *args, **kwargs):

        start = request.query_params.get("start", None)
        end = request.query_params.get("end", None)
        employee_id = self.kwargs.get("pk", None)

        if start == None or end == None or employee_id == None:
            return Response(status=400)
        else:
            start_date = datetime.strptime(start, "%Y-%m-%d").date()
            end_date = datetime.strptime(end, "%Y-%m-%d").date()
            working_hours = get_employee_working_hours(start_date, end_date, employee_id)
            employee = self.Employee.objects.get(pk=employee_id)
            employee = model_to_dict(employee)

            data = {
                "start": start,
                "end": end,
                "employee": employee,
                "working_hours": working_hours
            }
            return JsonResponse(data)"""
