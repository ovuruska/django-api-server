Daily Capacity API Documentation
================================

Overview
--------

The Daily Capacity API is designed to provide information about the available capacity for the services offered by our company. This API accepts four inputs, including two optional inputs (branches and employees) and two required inputs (service and start). The available services are 'We Wash' and 'Full Grooming'. The API returns a list of available capacities for the specified branches and services.

API Endpoint
------------


```bash
POST /api/v1/daily_capacity
```

Request Parameters
------------------

1.  `branches` (optional): A list of integers representing the branch IDs for which the available capacity should be returned. If not provided, the API will return the capacity for all branches.
2.  `employees` (optional): A list of integers representing the employee IDs for which the available capacity should be returned. If not provided, the API will return the capacity for all employees.
3.  `service` (required): A string representing the type of service. The available service options are:
    *   `'We Wash'`: For We Wash services
    *   `'Full Grooming'`: For Full Grooming services
4.  `date` (required): A string representing the starting date for the requested capacity data in the format `YYYY-MM-DD`.

Request Example
---------------


```json
{
  "branches": [1, 2],
  "employees": [3, 4],
  "service": "We Wash",
  "date": "2023-04-01"
}
```

Response
--------

The API response will be a JSON list of objects containing the date, branch, afternoon\_capacity, and morning\_capacity.

*   `date`: A string representing the date in the format `YYYY-MM-DD`.
*   `branch`: An integer representing the branch ID.
*   `afternoon_capacity`: A float (0 to 1) representing the available capacity for the afternoon time slot.
*   `morning_capacity`: A float (0 to 1) representing the available capacity for the morning time slot.

### Response Example


```json
[
  {
    "date": "2023-04-01",
    "branch": 1,
    "afternoon_capacity": 0.5,
    "morning_capacity": 0.2
  },
  {
    "date": "2023-04-01",
    "branch": 2,
    "afternoon_capacity": 0.4,
    "morning_capacity": 0.1
  }
]
```

Error Handling
--------------

If any of the required parameters are missing or invalid, the API will return an error message with an appropriate HTTP status code and a description of the error.

### Example Error Response


```json
{
  "error": "Invalid or missing parameters",
  "message": "The 'service' parameter is missing or has an invalid value. Please provide a valid value."
}
```
