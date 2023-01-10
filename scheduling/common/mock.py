from faker import Faker

from scheduling import models


class Mock:

	def __init__(self,
	             number_of_branches: int = 5,
	             number_of_employees: int = 25,
	             number_of_customers: int = 50,
	             number_of_dogs: int = 100,
	             number_of_appointments: int = 100,
	             number_of_services: int = 10,
	             number_of_products: int = 10,
	             ):
		self.number_of_branches = number_of_branches
		self.number_of_employees = number_of_employees
		self.number_of_customers = number_of_customers
		self.number_of_dogs = number_of_dogs
		self.number_of_services = number_of_services
		self.number_of_products = number_of_products
		self.number_of_appointments = number_of_appointments

	def generate(
			self
	):
		"""
			Generates mock data for testing purposes
			:returns: {
				'branches': [Branch, Branch, ...],
				'employees': [Employee, Employee, ...],
				'customers': [Customer, Customer, ...],
				'dogs': [Dog, Dog, ...],
				'services': [Service, Service, ...],
				'products': [Product, Product, ...],
				'appointments': [Appointment, Appointment, ...],
			}
		"""
		branches = []
		employees = []
		customers = []
		dogs = []
		services = []
		products = []
		appointments = []

		fake = Faker()

		for ind in range(self.number_of_branches):
			branch = models.Branch(
				name=fake.company(),
				address=fake.address(),
				description=fake.text(),
				tubs=fake.random_int(min=1, max=10),
			)
			branch.save()
			branches.append(branch)

		for ind in range(self.number_of_employees):
			employee = models.Employee(
					name=fake.name(),
					branch=branches[fake.random_int(min=0, max=self.number_of_branches - 1)],
					phone=fake.phone_number(),
					email=fake.email(),
					role=
					models.Employee.Role.choices[fake.random_int(min=0, max=len(models.Employee.Role.choices) - 1)][0],
					uid=fake.uuid4()
				)
			employee.save()
			employees.append(employee)

		for ind in range(self.number_of_customers):
			customer = models.Customer(
					name=fake.name(),
					phone=fake.phone_number(),
					email=fake.email(),
					uid=fake.uuid4(),
					address=fake.address(),
				)
			customer.save()
			customers.append(customer)

		for ind in range(self.number_of_dogs):
			dog = models.Dog(
				name=fake.name(),
				owner=customers[fake.random_int(min=0, max=self.number_of_customers - 1)],
				breed=fake.word(),
				weight=fake.random.normalvariate(80, 20),
				age=fake.random_int(min=1, max=20),
			)
			dog.save()
			dogs.append(
				dog
			)

		for ind in range(self.number_of_services):
			service = models.Service(
					name=fake.word(),
					description=fake.text(),
					cost=fake.pyfloat(positive=True, min_value=1, max_value=100),
					duration=fake.time_delta(),
				)
			service.save()
			services.append(service)

		for ind in range(self.number_of_products):
			product = models.Product(
					name=fake.word(),
					description=fake.text(),
					cost=fake.pyfloat(positive=True, min_value=1, max_value=100),
				)
			product.save()
			products.append(product)

		for ind in range(self.number_of_appointments):

			appointment = models.Appointment(
				branch = branches[fake.random_int(min=0, max=self.number_of_branches - 1)],
				employee=employees[fake.random_int(min=0, max=self.number_of_employees - 1)],
				dog=dogs[fake.random_int(min=0, max=self.number_of_dogs - 1)],
				start=fake.date_time(),
				end=fake.date_time(),
				customer = customers[fake.random_int(min=0, max=self.number_of_customers - 1)],
				customer_notes=fake.text(),
				employee_notes=fake.text(),
				cost = fake.pydecimal(positive=True, min_value=1, max_value=250),
				tip = fake.pydecimal(positive=True, min_value=1, max_value=100),
				status=models.Appointment.Status.choices[
					fake.random_int(min=0, max=len(models.Appointment.Status.choices) - 1)][
					0],
				appointment_type=models.Appointment.AppointmentType.choices[
					fake.random_int(min=0, max=len(models.Appointment.AppointmentType.choices) - 1)][0],

			)

			appointment_services = fake.random.choices(services, k=fake.random_int(min=0, max=4))

			appointment.save()
			for appointment_service in appointment_services:
				appointment.services.add(appointment_service)
			appointment_products = fake.random.choices(products, k=fake.random_int(min=0, max=4))
			for appointment_product in appointment_products:
				appointment.products.add(appointment_product)

			appointments.append(appointment)

		return {
			'branches': branches,
			'employees': employees,
			'customers': customers,
			'dogs': dogs,
			'services': services,
			'appointments': appointments,
			'products': products,

		}


	def remove(self,generated_data):
		"""
			Removes all data from the database
		"""
		for appointment in generated_data['appointments']:
			appointment.delete()
		for product in generated_data['products']:
			product.delete()
		for service in generated_data['services']:
			service.delete()
		for dog in generated_data['dogs']:
			dog.delete()
		for customer in generated_data['customers']:
			customer.delete()
		for employee in generated_data['employees']:
			employee.delete()
		for branch in generated_data['branches']:
			branch.delete()