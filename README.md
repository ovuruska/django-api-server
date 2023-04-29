Quicker Backend
==============


This Django project is a comprehensive scheduling and management application for appointments, transactions, and capacity planning. It features various APIs and modules that help manage the app's functionality, including analytics, authorization, search, and more.

Quicker Backend

======================

[![Test, Build and Push Docker Image](https://github.com/make-quicker/backend/actions/workflows/deploy.yml/badge.svg)](https://github.com/make-quicker/backend/actions/workflows/deploy.yml)
This README file contains instructions on how to set up and run our project's backend server on a local device. We utilize two different servers for different purposes: a SAM (Serverless Application Model) server to simulate AWS Lambda calls, and a naive Django server for testing and documentation purposes. Each server has its own setup and configuration requirements, which are outlined below.

SAM Server Setup
----------------

The SAM server is used for development purposes, allowing developers to test and debug their code locally by simulating AWS Lambda calls.

### Prerequisites

*   AWS CLI
*   AWS SAM CLI

### Configuration

1.  Configure your `.env.dev` file with your desired development environment settings.
2.  Rename the `.env.dev` file to `.env` so that the SAM server can use it.

### Running the SAM Server

To run the SAM server, simply execute the following command in your terminal:

```bash
bash run.sh
```

This will start the SAM server locally, allowing you to test and debug your Lambda functions.

Naive Django Server Setup
-------------------------

The naive Django server is used for testing and documentation purposes, enabling you to run tests and view the Swagger/ReDoc API documentation.

### Prerequisites

*   Python 3
*   Django
*   pip

### Configuration

1.  Copy the `.env.test` file to a new file named `.env`.
2.  Configure the naive Django server by editing the `.env` file with your desired test environment settings.

### Running the Naive Django Server

To run the naive Django server, execute the following command in your terminal:

```bash
python manage.py runserver
```

This will start the Django server locally, allowing you to run tests and view the Swagger/ReDoc API documentation.

Server Missions
---------------

As mentioned earlier, our backend utilizes two different servers for different purposes:

*   **SAM Server**: Used for development purposes, allowing developers to simulate AWS Lambda calls and debug their code locally.
*   **Naive Django Server**: Used for testing and documentation purposes, enabling you to run tests and view the Swagger/ReDoc API documentation.

Please ensure that you follow the appropriate setup and configuration instructions for each server depending on your intended use.

