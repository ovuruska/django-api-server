# Add Admin Command for Django

Overview
--------

The `add_admin` command is a custom Django management command designed to create a new admin employee and store it in the database. It takes the required input from the command line interface (CLI), including username, password, and email, and populates the rest of the employee's details using the Faker library. The command is useful for initializing an admin user in the scheduling application.

Usage
-----

To execute the `add_admin` command, run the following command in your terminal:

`python manage.py add_admin`

You will be prompted to enter the admin's username, password, and email. After providing the required information, the command will create a new admin user and store it in the database.

Code Breakdown
--------------

1.  Import necessary modules:

*   `BaseCommand` from `django.core.management.base` is the base class for creating custom Django management commands.
*   `Faker` from the `faker` library is used to generate random fake data.
*   `User` from `django.contrib.auth.models` is the Django's default user model.
*   `Roles` from `common.roles` is an enumeration of user roles.
*   `models` from the `scheduling` module contains the `Employee` model definition.

2.  Define the `Command` class, which inherits from `BaseCommand`:

*   The `help` attribute provides a brief description of the command.
*   The `handle` method is where the core functionality of the command resides.

3.  In the `handle` method:

*   Collect the required input from the CLI: username, password, and email.
*   Create a `Faker` instance.
*   Create an `Employee` instance with the following attributes:
    *   `name`: a randomly generated name using the Faker library
    *   `phone`: a randomly generated phone number using the Faker library
    *   `role`: set to `Roles.ADMIN`
    *   `email`: provided by the user
    *   `user`: a new `User` instance created with the provided username, password, and email
    *   `uid`: a randomly generated UUID using the Faker library
*   Save the created `Employee` instance to the database.

Requirements
------------

To use this custom Django command, you need to have the following dependencies installed:

*   Django (version 3.0 or higher)
*   Faker (version 4.0 or higher)



