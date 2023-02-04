from rest_framework import generics
from scheduling.models.branch_working_hour import BranchWorkingHour
from scheduling.serializers.Branch_Working_Hour import BranchWorkingHourSerializer


class BranchWorkingHourCreate(generics.CreateAPIView, generics.ListAPIView):
    queryset = BranchWorkingHour.objects.all()
    serializer_class = BranchWorkingHourSerializer
