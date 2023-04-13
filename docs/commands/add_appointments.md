# Add Appointments Command for Django

Overview
--------

The `add_appointments` command is a custom Django management command designed to create a specified number of appointments with a specific status and store them in the database. The command is useful for populating the database with appointments for testing and development purposes.

Usage
-----

To execute the `add_appointments` command, run the following command in your terminal:

php

```shell
python manage.py add_appointments <amount> <status>
```

Replace `<amount>` with the number of appointments you want to create and `<status>` with the desired status for the appointments. The command will create the specified number of appointments with the given status and store them in the database.

Code Breakdown
--------------

1.  Import necessary modules:

*   `BaseCommand` and `CommandError` from `django.core.management.base` are used for creating custom Django management commands and handling errors.
*   `timezone` from `django.utils` is used for creating timezone-aware datetime objects.
*   `random` is used for generating random selections.
*   Import necessary models from the `scheduling` module.

2.  Define the `Command` class, which inherits from `BaseCommand`:

*   The `help` attribute provides a brief description of the command.
*   The `add_arguments` method defines the command-line arguments that the command accepts.
*   The `handle` method is where the core functionality of the command resides.

3.  In the `add_arguments` method:

*   Define two required arguments: `amount` (integer) and `status` (string).

4.  In the `handle` method:

*   Get the `amount` and `status` arguments from the `options` dictionary.
*   Check if the given `status` is valid by comparing it to the available statuses in the `Appointment.Status` enumeration. If not, raise a `CommandError`.
*   Fetch all related objects (Customers, Dogs, Branches, Employees, Services, and Products) from the database and store them in lists.
*   Check if the required related objects are present. If not, raise a `CommandError`.
*   For each appointment to be created:
    *   Create an `Appointment` instance with random related objects and the specified status.
    *   Save the appointment to the database.
    *   Set random services and products for the appointment.
    *   Save the appointment again to store the many-to-many relationships.
*   Display a success message indicating the number of appointments created and their status.

Requirements
------------

To use this custom Django command, you need to have the following dependencies installed:

*   Django (version 3.0 or higher)% 