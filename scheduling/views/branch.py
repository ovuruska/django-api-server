from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from scheduling.models import Branch
from scheduling.serializers.Branch import BranchSerializer


class BranchRetrieveModifyAPIView(RetrieveAPIView,ListAPIView,DestroyAPIView,UpdateAPIView):
	serializer_class = BranchSerializer
	queryset = Branch.objects.all()

	def get(self, request, *args, **kwargs):
		if self.kwargs['pk'] == 'all':
			return self.list(request, *args, **kwargs)
		else:
			return self.retrieve(request, *args, **kwargs)

class BranchCreateAPIView(CreateAPIView):
	serializer_class = BranchSerializer
	queryset = Branch.objects.all()

