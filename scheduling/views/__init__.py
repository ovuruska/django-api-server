from .appointment import *
from .branch_get import BranchRetrieveAPIView
from .branch_modify import BranchModifyAPIView
from .customer import CustomerRetrieveAPIView, CustomerDogsRetrieveAPIView
from .dog import DogCreateAPIView, DogModifyRetrieveDestroyAPIView
from .employee import *
from .product import *
from .schedule import ScheduleCustomerListRetrieveView
from .service import *


class BranchListAllAPIView:
	pass