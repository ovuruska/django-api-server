from datetime import datetime
from django.test import TestCase

from capacity.selectors.monthly_capacity import WorkInterval, CapacityTask, CapacityCalculationParams, \
	get_capacity_between_interval


class TestMonthlyCapacityMultipleWorkers(TestCase):
	delta = 0.01

	def test_scenario_1_multiple_workers(self):
		# Test get_capacity_between_interval function with multiple worker_ids and 3 days
		start_date = datetime(2023, 4, 1)
		end_date = datetime(2023, 4, 3)

		work_intervals = [
			WorkInterval(datetime(2023, 4, 1, 9), datetime(2023, 4, 1, 18), 1),
			WorkInterval(datetime(2023, 4, 2, 9), datetime(2023, 4, 2, 18), 1),
			WorkInterval(datetime(2023, 4, 3, 9), datetime(2023, 4, 3, 18), 1),
			WorkInterval(datetime(2023, 4, 1, 9), datetime(2023, 4, 1, 18), 2),
			WorkInterval(datetime(2023, 4, 2, 9), datetime(2023, 4, 2, 18), 2),
			WorkInterval(datetime(2023, 4, 3, 9), datetime(2023, 4, 3, 18), 2),
		]

		tasks = [
			CapacityTask(datetime(2023, 4, 1, 10), datetime(2023, 4, 1, 12), 1),
			CapacityTask(datetime(2023, 4, 2, 14), datetime(2023, 4, 2, 16), 1),
			CapacityTask(datetime(2023, 4, 3, 11), datetime(2023, 4, 3, 13), 1),
			CapacityTask(datetime(2023, 4, 1, 13), datetime(2023, 4, 1, 15), 2),
			CapacityTask(datetime(2023, 4, 2, 10), datetime(2023, 4, 2, 12), 2),
			CapacityTask(datetime(2023, 4, 3, 14), datetime(2023, 4, 3, 16), 2),
		]

		params = CapacityCalculationParams(start_date, end_date, work_intervals, tasks)
		result = get_capacity_between_interval(params)
		self.assertEqual(len(result), 3)

		# Day 1, Worker 1
		self.assertEqual(result[0]['date'], '2023-04-01')
		self.assertAlmostEqual(result[0]['morning_capacity'], 0.36, delta=self.delta)
		self.assertAlmostEqual(result[0]['afternoon_capacity'], 0.22, delta=self.delta)

		# Day 2, Worker 1
		self.assertEqual(result[1]['date'], '2023-04-02')
		self.assertAlmostEqual(result[1]['morning_capacity'], 0.27, delta=self.delta)
		self.assertAlmostEqual(result[1]['afternoon_capacity'], 0.22, delta=self.delta)

		# Day 3, Worker 1
		self.assertEqual(result[2]['date'], '2023-04-03')
		self.assertAlmostEqual(result[2]['morning_capacity'], 0.27, delta=self.delta)
		self.assertAlmostEqual(result[2]['afternoon_capacity'], 0.27, delta=self.delta)


	def test_multiple_workers_with_no_work_intervals_with_tasks(self):
		# Test get_capacity_between_interval function with multiple worker_ids and 3 days
		start_date = datetime(2023, 4, 1)
		end_date = datetime(2023, 4, 3)

		work_intervals = [

		]
		tasks = [
			CapacityTask(datetime(2023, 4, 1, 10), datetime(2023, 4, 1, 12), 1),
			CapacityTask(datetime(2023, 4, 2, 14), datetime(2023, 4, 2, 16), 1),
			]
		params = CapacityCalculationParams(start_date, end_date, work_intervals, tasks)
		result = get_capacity_between_interval(params)
		self.assertEqual(len(result), 3)
		self.assertEqual(result[0]['date'], '2023-04-01')
		self.assertAlmostEqual(result[0]['morning_capacity'],1, delta=self.delta)
		self.assertAlmostEqual(result[0]['afternoon_capacity'], 1, delta=self.delta)
		self.assertEqual(result[1]['date'], '2023-04-02')
		self.assertAlmostEqual(result[1]['morning_capacity'], 1, delta=self.delta)
		self.assertAlmostEqual(result[1]['afternoon_capacity'], 1, delta=self.delta)
		self.assertEqual(result[2]['date'], '2023-04-03')
		self.assertAlmostEqual(result[2]['morning_capacity'], 1, delta=self.delta)
		self.assertAlmostEqual(result[2]['afternoon_capacity'], 1, delta=self.delta)



	def test_multiple_workers_with_no_work_intervals_with_full_capacity(self):
		# Test get_capacity_between_interval function with multiple worker_ids and 3 days
		start_date = datetime(2023, 4, 1)
		end_date = datetime(2023, 4, 3)

		work_intervals = [
			WorkInterval(datetime(2023, 4, 1, 10), datetime(2023, 4, 1, 12), 1),
			WorkInterval(datetime(2023, 4, 2, 14), datetime(2023, 4, 2, 16), 1),
			WorkInterval(datetime(2023, 4, 3, 10), datetime(2023, 4, 1, 12), 1),
			WorkInterval(datetime(2023, 4, 1, 14), datetime(2023, 4, 2, 16), 2),
			WorkInterval(datetime(2023, 4, 2, 10), datetime(2023, 4, 1, 12), 2),
			WorkInterval(datetime(2023, 4, 3, 14), datetime(2023, 4, 2, 16), 2),
		]
		tasks = [
			CapacityTask(datetime(2023, 4, 1, 13), datetime(2023, 4, 1, 15), 1),
			CapacityTask(datetime(2023, 4, 2, 8), datetime(2023, 4, 2, 10), 1),
			]
		params = CapacityCalculationParams(start_date, end_date, work_intervals, tasks)
		result = get_capacity_between_interval(params)
		self.assertEqual(len(result), 3)
		self.assertEqual(result[0]['date'], '2023-04-01')
		self.assertAlmostEqual(result[0]['morning_capacity'],0, delta=self.delta)
		self.assertAlmostEqual(result[0]['afternoon_capacity'], 0, delta=self.delta)
		self.assertEqual(result[1]['date'], '2023-04-02')
		self.assertAlmostEqual(result[1]['morning_capacity'], 0, delta=self.delta)
		self.assertAlmostEqual(result[1]['afternoon_capacity'], 0, delta=self.delta)
		self.assertEqual(result[2]['date'], '2023-04-03')
		self.assertAlmostEqual(result[2]['morning_capacity'], 0, delta=self.delta)
		self.assertAlmostEqual(result[2]['afternoon_capacity'], 0, delta=self.delta)

