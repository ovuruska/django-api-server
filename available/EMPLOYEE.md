

Get available employees API Documentation
=================

Endpoint
--------

**POST** `api/available/employees`

Description
-----------

This endpoint retrieves the available employees based on the given date, branch IDs, and service type. The response will include the branch and employee details for each available employee.

Request
-------

### Headers

| Name | Type | Description |
| --- | --- | --- |
| Content-Type | String | Must be `application/json`. |


### Body


| Name | Type | Description | Required |
| --- | --- | --- | --- |
| date | String | Date and time in the format `dd-mm-YYYY HH:MM` to check availability. | Yes |
| branches | Array of Int | An array containing the branch IDs to search for available employees. | No |
| service | String | The type of service for which employees are needed (One of "Full Grooming" | "We Wash"). | Yes | 

#### Example

```json
{
  "date": "12-05-2023 14:00",
  "branches": [1, 2, 3],
  "service": "Full Grooming"
}
```

Response
--------

### Status Codes

```
| Code | Description |
| --- | --- |
| 200 | Successful request, returns data. |
| 400 | Bad request, invalid input parameters. |
| 500 | Internal server error. |
```

### Body

An array of objects containing the branch and employee details for each available employee.


| Name | Type | Description |
| --- | --- | --- |
| branch | Object | The branch information. |
| branch.id | Int | The ID of the branch. |
| branch.name | String | The name of the branch. |
| employee | Object | The employee information. |
| employee.id | Int | The ID of the employee. |
| employee.name | String | The name of the employee. |


#### Example



```json
[
  {
    "branch": {
      "id": 1,
      "name": "Downtown Groomers"
    },
    "employee": {
      "id": 101,
      "name": "John Doe"
    }
  },
  {
    "branch": {
      "id": 3,
      "name": "Uptown Groomers"
    },
    "employee": {
      "id": 301,
      "name": "Jane Smith"
    }
  }
]
```