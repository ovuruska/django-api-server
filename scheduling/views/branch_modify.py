from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView

from ..models import Branch
from ..serializers.Branch import BranchSerializer


class BranchModifyAPIView(CreateAPIView,DestroyAPIView,UpdateAPIView):
	serializer_class = BranchSerializer
	queryset = Branch.objects.all()

