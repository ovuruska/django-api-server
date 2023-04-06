Daily Available Slots API Documentation
=======================================

Overview
--------

The Daily Available Slots API is designed to retrieve the available slots information of employees and branches for a specific service and date. This API accepts the service name and date in the form of a string (YYYY-mm-dd) as required inputs, along with optional employee and branch IDs. The response will include the appointment slots list of the given date. Appointment slots have start and end fields, in the format `YYYY-mm-ddThh:MM`. Employee and branch objects are also included in the response.

Endpoint
--------

**POST** `/api/available/daily`

Request Parameters
------------------

*   **employees** (optional): A list of integers representing the employee IDs. Default is an empty list `[]`.
*   **branches** (optional): A list of integers representing the branch IDs. Default is an empty list `[]`.
*   **service** (required): A string representing the service name.
*   **date** (required): A string representing the target date in the format `YYYY-mm-dd`.
*   **duration** (optional): An integer representing the duration of the appointment in minutes. Default is 60 minutes.
*  **times** (optional): A list of strings representing the time of day. Default is an empty list `[]`. Possible values are: "Morning", "Afternoon", "Evening".

Example Request
---------------

json

json

```json
{
  "employees": [1, 2, 3],
  "branches": [101, 102],
  "service": "Full Grooming",
  "date": "2023-04-01",
  "duration": 60,
    "times": ["Morning", "Afternoon"],
}
```

Response
--------

The API returns a JSON array containing the available appointment slots for the specified date. Each appointment slot includes the start time, end time, employee object, and branch object.

### Example Response

json

json

```json
[
  {
    "start": "2023-04-01T09:00",
    "end": "2023-04-01T10:00",
    "employee": 1,
    "branch": 2
  },
  ...
]
```

Errors
------

Possible errors and their descriptions:

*   **400 Bad Request**: The request was malformed or invalid. Check the required fields (service and date) and their format.
*   **500 Internal Server Error**: An error occurred on the server side. Please try again later or contact support if the issue persists.