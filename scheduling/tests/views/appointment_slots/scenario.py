import datetime

from common.auth_test_case import CustomerAuthTestCase
from common.roles import Roles
from scheduling.models import Branch, Employee, EmployeeWorkingHour, Dog, Appointment


class ScenarioTestCase(CustomerAuthTestCase):

    @staticmethod
    def get_now() -> str:

        now = datetime.datetime.now().replace(microsecond=0, second=0)
        formatted_time = now.strftime("%Y-%m-%d")
        return formatted_time

    @staticmethod
    def format_time(time: datetime.datetime) -> str:
        # 2023-02-01T00:00:00
        formatted_time = time.strftime("%Y-%m-%d")
        return formatted_time
    def setUp(self):
        super().setUp()

        self.pet = Dog.objects.create(
            name='Bella',
            owner=self.customer
        )

        self.branch_1 = Branch.objects.create(
            name='Royal Oaks',
        )
        self.branch_2 = Branch.objects.create(
            name='Bellaire',
        )
        self.branch_3 = Branch.objects.create(
            name='Westchase',
        )
        self.employee_1 = Employee.objects.create(
            name='Jonathan Beck',
            branch=self.branch_1,
            role=Roles.EMPLOYEE_FULL_GROOMING,
        )
        start = datetime.datetime.now().replace(hour=8)
        end = start.replace(20)
        
        for i in range(5):
            
            EmployeeWorkingHour.objects.update_or_create(
                employee=self.employee_1,
                week_day=i,
                start = start,
                end = end,
                branch=self.branch_1)

        EmployeeWorkingHour.objects.update_or_create(
            employee=self.employee_1,
            week_day=6,
            start=start,
            end=end,
            branch=self.branch_2)

        self.employee_2 = Employee.objects.create(
            name='Allison Pena',
            branch=self.branch_1,
            role=Roles.EMPLOYEE_FULL_GROOMING,
        )
        for i in range(3):
            EmployeeWorkingHour.objects.update_or_create(
                employee=self.employee_2,
                week_day=i,
                start=start,
                end=end,
                branch=self.branch_2)

        EmployeeWorkingHour.objects.update_or_create(
            employee=self.employee_2,
            start=start,
            end=end,
            week_day=4,
            branch=self.branch_1)

        EmployeeWorkingHour.objects.update_or_create(
            employee=self.employee_2,
            start=start,
            end=end,
            week_day=5,
            branch=self.branch_1)

        self.employee_3 = Employee.objects.create(
            name='Luisa Mccoy',
            branch=self.branch_1,
            role=Roles.EMPLOYEE_WE_WASH,
        )
        for i in range(5):
            EmployeeWorkingHour.objects.update_or_create(
                employee=self.employee_3,
                start=start,
                end=end,
                week_day=i,
                branch=self.branch_3)

        self.employee_4 = Employee.objects.create(
            name='Jane Doe',
            branch=self.branch_1,
            role=Roles.EMPLOYEE_WE_WASH,
        )
        for i in range(5):
            EmployeeWorkingHour.objects.update_or_create(
                employee=self.employee_4,
                start=start,
                week_day=i,
                end=end,
                branch=self.branch_1)

        # Create appointments for future dates at most 1 week from now
        for i in range(1, 40):
            ind = i % 7
            employee = [self.employee_1, self.employee_2, self.employee_3, self.employee_4][i % 4]
            Appointment.objects.create(
                employee=employee,
                customer=self.customer,
                branch=self.branch_1,
                dog=self.pet,
                start=datetime.datetime.combine(
                    datetime.date.today() + datetime.timedelta(days=ind),
                    datetime.time(8, 0, 0)
                ),
                end=datetime.datetime.combine(
                    datetime.date.today() + datetime.timedelta(days=ind),
                    datetime.time(16, 0, 0)
                ),
                appointment_type="Full Grooming",
            )

    @staticmethod
    def get_now() -> str:

        now = datetime.datetime.now().replace(microsecond=0, second=0)
        formatted_time = now.strftime("%Y-%m-%d")
        return formatted_time

    @staticmethod
    def format_time(time: datetime.datetime) -> str:
        # 2023-02-01T00:00:00
        formatted_time = time.strftime("%Y-%m-%d")
        return formatted_time
