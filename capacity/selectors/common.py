from datetime import datetime


class CapacityTask:
	def __init__(self, start, end, worker: int, ):
		self.start: datetime = start
		self.end: datetime = end
		self.worker: int = worker


class TaskWorker:
	def __init__(self, start, end, id: int, ):
		self.start: datetime = start
		self.end: datetime = end
		self.id: int = id


class WorkInterval:
	def __init__(self, start, end, worker_id):
		self.start: datetime = start
		self.end: datetime = end
		self.worker_id: int = worker_id


class CapacityCalculationParams:
	def __init__(self, start_date: datetime, end_date: datetime, intervals: [WorkInterval], tasks: [CapacityTask]):
		self.start_date = start_date
		self.end_date = end_date
		self.intervals = intervals
		self.tasks = tasks
