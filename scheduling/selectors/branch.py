from scheduling.models import Branch


def get_branch_by_name(branch_name):
	"""
	:param branch_name: name of the branch
	:return: branch
	"""
	return Branch.objects.get(name=branch_name)