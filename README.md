

Quicker Backend
==============

This Django project is a comprehensive scheduling and management application for appointments, transactions, and capacity planning. It features various APIs and modules that help manage the app's functionality, including analytics, authorization, search, and more.

Table of Contents
-----------------

*   [Getting Started](#getting-started)
    *   [Prerequisites](#prerequisites)
    *   [Installation](#installation)
*   [Usage](#usage)
*   [API Endpoints](#api-endpoints)
*   [Contributing](#contributing)
*   [License](#license)

Getting Started
---------------

These instructions will help you set up the project on your local machine for development and testing purposes.

### Prerequisites

*   Python 3.7 or later
*   Docker
*   Docker Compose

### Installation

1.  Clone the repository:

bash

```bash
git clone https://github.com/make-quicker/backend.git
cd backend
```

2.  Build and run Docker containers:

bash

```bash
docker-compose -f dev.docker-compose.yml up --build
```

The application should now be running at `http://localhost:8000/`.

Usage
-----

You can interact with the APIs by sending requests to the provided endpoints. For more information on available endpoints, see the [API Endpoints](#api-endpoints) section.

API Endpoints
-------------

Here's a list of the main API endpoints:

*   `/api/analytics/`: Analytics API for generating insights and reporting
*   `/api/authorization/`: Authorization API for managing authentication and user permissions
*   `/api/capacity/`: Capacity API for managing and calculating resource capacity
*   `/api/scheduling/`: Scheduling API for managing appointments and availability
*   `/api/search/`: Search API for querying and filtering data
*   `/api/transactions/`: Transactions API for managing appointment transactions.

Contributing
------------

We welcome contributions from the community. To get started, please fork the repository, create a new branch for your changes, and submit a pull request when you're ready.

License
-------

This project is licensed under the [MIT License](LICENSE). Please refer to the license file for more information.
