Monthly Capacity API Documentation
==================================

Overview
--------

The Monthly Capacity API is designed to retrieve the capacity information of employees and branches for a specific service and month. This API accepts the service name and date in the form of a string (mm/YYYY) as required inputs, along with optional employee and branch IDs. The response will include the capacity details of the morning and afternoon sessions for the specified month.

Endpoint
--------

**POST** `/api/schedule/capacity/monthly`

Request Parameters
------------------

*   **employees** (optional): A list of integers representing the employee IDs. Default is an empty list `[]`.
*   **branches** (optional): A list of integers representing the branch IDs. Default is an empty list `[]`.
*   **service** (required): A string representing the service name.
*   **date** (required): A string representing the target month and year in the format `mm/YYYY`.

Example Request
---------------

json

```json
{
  "employees": [1, 2, 3],
  "branches": [101, 102],
  "service": "haircut",
  "date": "04/2023"
}
```

Response
--------

The API returns a JSON array containing the capacity details for each day of the specified month. Each day includes the date (in `YYYY-mm-dd` format), morning capacity, and afternoon capacity.

### Example Response

json

```json
[
  {
    "date": "2023-04-01",
    "morning_capacity": 0.5,
    "afternoon_capacity": 0.9
  },
  {
    "date": "2023-04-02",
    "morning_capacity": 0.6,
    "afternoon_capacity": 0.8
  }
]
```

If capacity information is 1, then it means that the day is fully booked. If capacity information is 0, then it means that the day is fully available. Capacity calculation
is made based on available appointments and working hours of employees and branches.

Errors
------

Possible errors and their descriptions:

*   **400 Bad Request**: The request was malformed or invalid. Check the required fields (service and date) and their format.
*   **500 Internal Server Error**: An error occurred on the server side. Please try again later or contact support if the issue persists.
