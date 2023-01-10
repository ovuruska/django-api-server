from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from scheduling.models import Branch
from scheduling.serializers.Branch import BranchSerializer


class BranchRetrieveAPIView(ListAPIView):
	serializer_class = BranchSerializer

	def get_queryset(self):
		if(self.kwargs['pk'] == 'all'):
			return Branch.objects.all()
		else:
			try:
				return Branch.objects.filter(pk=self.kwargs['pk'])
			except ValueError:
				return Branch.objects.none()


class BranchCreateAPIView(CreateAPIView):
	serializer_class = BranchSerializer
	queryset = Branch.objects.all()


class BranchModifyAPIView(DestroyAPIView,UpdateAPIView):
	serializer_class = BranchSerializer
	queryset = Branch.objects.all()
