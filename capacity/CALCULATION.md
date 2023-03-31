Capacity Calculation Module
===========================

This module provides a set of classes and functions to calculate the capacity of employees in a scheduling system. It calculates the daily and monthly capacity for a given set of employees based on their working hours and scheduled appointments.

Classes
-------

1.  `CapacityTask`: Represents a task with a start and end time, and a worker ID.
2.  `TaskWorker`: Represents a worker with a start and end time, and an ID.
3.  `WorkInterval`: Represents a working interval with a start and end time, and a worker ID.
4.  `CapacityCalculationParams`: Contains the parameters required for capacity calculation, including the start and end date, work intervals, and tasks.

Functions
---------

1.  `get_monthly_capacity(date, employees)`: Calculates the monthly capacity for a given set of employees. Returns a list of daily capacities.
    
2.  `get_tasks(appointments: [Appointment]) -> [CapacityTask]`: Extracts tasks from appointments.
    
3.  `get_work_intervals(working_hours: [EmployeeWorkingHour], date=None) -> [WorkInterval]`: Converts working hours into work intervals.
    
4.  `get_total_slots(start: datetime, end: datetime, interval: int) -> int`: Calculates the total number of slots in a given time interval.
    
5.  `convert_time(start: datetime, end: datetime, interval: int)`: Returns a function to convert a time range into start and end indices in the given interval.
    
6.  `get_capacity_between_interval(params: CapacityCalculationParams)`: Calculates the capacity between a given interval.
    
7.  `get_daily_capacity(date, intervals, tasks)`: Calculates the daily capacity for a given date, intervals, and tasks.
    
8.  `get_morning_capacity(intervals, tasks)`: Calculates the morning capacity for a given set of intervals and tasks.
    
9.  `get_afternoon_capacity(intervals, tasks)`: Calculates the afternoon capacity for a given set of intervals and tasks.
    
10.  `get_capacity(intervals, tasks, start_hour: int, end_hour: int, step: int)`: Calculates the capacity for a given set of intervals, tasks, start hour, end hour, and step.
    

Usage
-----

To calculate the monthly capacity for a set of employees, simply call the `get_monthly_capacity(date, employees)` function. This will return a list of daily capacities for the given month.

python

```python
from capacity_calculation import get_monthly_capacity

date = datetime(2023, 3, 1)
employees = [1, 2, 3]
monthly_capacity = get_monthly_capacity(date, employees)

print(monthly_capacity)
```

This will output the daily capacities for each day in the month:

css

```css
[  {'date': '2023-03-01', 'morning_capacity': 0.6, 'afternoon_capacity': 0.7},  {'date': '2023-03-02', 'morning_capacity': 0.5, 'afternoon_capacity': 0.8},  ...  {'date': '2023-03-31', 'morning_capacity': 0.7, 'afternoon_capacity': 0.6}]
```