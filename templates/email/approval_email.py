

text = """
Hi,
You have an appointment in {} at {}. If you are available,
click on {}.


If you want to cancel appointment, click on {}.


If you want appointment to be rescheduled, click on {}.

Cheers,
Oguz
"""

def approval_email(date,hour,accept_url,cancel_url,reschedule_url):
	return text.format(date,hour,accept_url,cancel_url,reschedule_url)

