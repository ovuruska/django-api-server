from datetime import timedelta

import pytz


def get_slots(hours, appointments, minutes=60):
	tz = pytz.UTC
	aware_hours = [(h.replace(tzinfo=tz) if h.tzinfo is None else h) for h in hours]

	# Ensure appointments are timezone-aware
	aware_appointments = [(start.replace(tzinfo=tz) if start.tzinfo is None else start,
	                       end.replace(tzinfo=tz) if end.tzinfo is None else end) for start, end in appointments]

	slots = sorted([(aware_hours[0], aware_hours[0])] + aware_appointments + [(aware_hours[1], aware_hours[1])])
	duration = timedelta(minutes=minutes)

	available_slots = []
	for start, end in ((slots[i][1], slots[i + 1][0]) for i in range(len(slots) - 1)):
		while start + duration <= end:
			available_slots.append([start, start + duration])
			start += duration
	return available_slots