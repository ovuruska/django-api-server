from datetime import datetime
from django.test import TestCase

from capacity.selectors.monthly_capacity import WorkInterval, CapacityTask, CapacityCalculationParams, \
	get_capacity_between_interval


class MonthlyCapacityTestSingleWorker(TestCase):
	delta = 0.1
	def test_scenario_1(self):

		# ... (all the code above remains the same)

		# Test get_capacity_between_interval function
		start_date = datetime(2023, 4, 1)
		end_date = datetime(2023, 4, 5)

		work_intervals = [
			WorkInterval(datetime(2023, 4, 1, 9), datetime(2023, 4, 1, 18), 1),
			WorkInterval(datetime(2023, 4, 2, 9), datetime(2023, 4, 2, 18), 1),
			WorkInterval(datetime(2023, 4, 3, 9), datetime(2023, 4, 3, 18), 1),
		]

		tasks = [
			CapacityTask(datetime(2023, 4, 1, 10), datetime(2023, 4, 1, 12), 1),
			CapacityTask(datetime(2023, 4, 2, 14), datetime(2023, 4, 2, 16), 1),
			CapacityTask(datetime(2023, 4, 3, 11), datetime(2023, 4, 3, 13), 1),
		]

		params = CapacityCalculationParams(start_date, end_date, work_intervals, tasks)
		result = get_capacity_between_interval(params)
		self.assertEqual(len(result), 5)
		self.assertEqual(result[0]['date'], '2023-04-01')
		self.assertAlmostEqual(result[0]['morning_capacity'], 0.55,delta = self.delta)
		self.assertAlmostEqual(result[0]['afternoon_capacity'], 0.0,delta = self.delta)
		self.assertEqual(result[1]['date'], '2023-04-02')
		self.assertAlmostEqual(result[1]['morning_capacity'], 0.0,delta = self.delta)
		self.assertAlmostEqual(result[1]['afternoon_capacity'], 0.45,delta = self.delta)
		self.assertEqual(result[2]['date'], '2023-04-03')
		self.assertAlmostEqual(result[2]['morning_capacity'], 0.55,delta = self.delta)
		self.assertAlmostEqual(result[2]['afternoon_capacity'], 0.1,delta = self.delta)
		self.assertEqual(result[3]['date'], '2023-04-04')
		self.assertAlmostEqual(result[3]['morning_capacity'], 1,delta = self.delta)
		self.assertAlmostEqual(result[3]['afternoon_capacity'], 1,delta = self.delta)
		self.assertEqual(result[4]['date'], '2023-04-05')
		self.assertAlmostEqual(result[4]['morning_capacity'], 1,delta = self.delta)
		self.assertAlmostEqual(result[4]['afternoon_capacity'], 1,delta = self.delta)

	def test_scenario_2(self):
		# Test get_capacity_between_interval function with more complex intervals and tasks
		start_date = datetime(2023, 4, 1)
		end_date = datetime(2023, 4, 10)

		work_intervals = [
			WorkInterval(datetime(2023, 4, 1, 9), datetime(2023, 4, 1, 18), 1),
			WorkInterval(datetime(2023, 4, 2, 9), datetime(2023, 4, 2, 18), 1),
			WorkInterval(datetime(2023, 4, 3, 9), datetime(2023, 4, 3, 18), 1),
			WorkInterval(datetime(2023, 4, 4, 9), datetime(2023, 4, 4, 14), 1),
			WorkInterval(datetime(2023, 4, 5, 13), datetime(2023, 4, 5, 18), 1),
			WorkInterval(datetime(2023, 4, 6, 9), datetime(2023, 4, 6, 18), 1),
			WorkInterval(datetime(2023, 4, 7, 9), datetime(2023, 4, 7, 12), 1),
		]

		tasks = [
			CapacityTask(datetime(2023, 4, 1, 10), datetime(2023, 4, 1, 12), 1),
			CapacityTask(datetime(2023, 4, 2, 14), datetime(2023, 4, 2, 16), 1),
			CapacityTask(datetime(2023, 4, 3, 11), datetime(2023, 4, 3, 13), 1),
			CapacityTask(datetime(2023, 4, 4, 10), datetime(2023, 4, 4, 12), 1),
			CapacityTask(datetime(2023, 4, 5, 15), datetime(2023, 4, 5, 17), 1),
			CapacityTask(datetime(2023, 4, 6, 13), datetime(2023, 4, 6, 15), 1),
			CapacityTask(datetime(2023, 4, 7, 10), datetime(2023, 4, 7, 11), 1),
			CapacityTask(datetime(2023, 4, 8, 16), datetime(2023, 4, 8, 17), 1),
			CapacityTask(datetime(2023, 4, 9, 10), datetime(2023, 4, 9, 14), 1),
			CapacityTask(datetime(2023, 4,10, 11), datetime(2023, 4, 10, 15), 1),
		]

		params = CapacityCalculationParams(start_date, end_date, work_intervals, tasks)
		result = get_capacity_between_interval(params)
		self.assertEqual(len(result), 10)

		# Day 1
		self.assertEqual(result[0]['date'], '2023-04-01')
		self.assertAlmostEqual(result[0]['morning_capacity'], 0.55, delta=self.delta)
		self.assertAlmostEqual(result[0]['afternoon_capacity'], 0.0, delta=self.delta)

		# Day 2
		self.assertEqual(result[1]['date'], '2023-04-02')
		self.assertAlmostEqual(result[1]['morning_capacity'], 0.0, delta=self.delta)
		self.assertAlmostEqual(result[1]['afternoon_capacity'], 0.45, delta=self.delta)

		# Day 3
		self.assertEqual(result[2]['date'], '2023-04-03')
		self.assertAlmostEqual(result[2]['morning_capacity'], 0.55, delta=self.delta)
		self.assertAlmostEqual(result[2]['afternoon_capacity'], 0.1, delta=self.delta)

		# Day 4
		self.assertEqual(result[3]['date'], '2023-04-04')
		self.assertAlmostEqual(result[3]['morning_capacity'], 0.55, delta=self.delta)
		self.assertAlmostEqual(result[3]['afternoon_capacity'], 0.0, delta=self.delta)

		# Day 5
		self.assertEqual(result[4]['date'], '2023-04-05')
		self.assertAlmostEqual(result[4]['morning_capacity'], 0.0, delta=self.delta)
		self.assertAlmostEqual(result[4]['afternoon_capacity'], 0.45, delta=self.delta)

		# Day 6
		self.assertEqual(result[5]['date'], '2023-04-06')
		self.assertAlmostEqual(result[5]['morning_capacity'], 0.2, delta=self.delta)
		self.assertAlmostEqual(result[5]['afternoon_capacity'], 0.45, delta=self.delta)

		# Day 7
		self.assertEqual(result[6]['date'], '2023-04-07')
		self.assertAlmostEqual(result[6]['morning_capacity'], 0.42, delta=self.delta)
		self.assertAlmostEqual(result[6]['afternoon_capacity'], 1, delta=self.delta)

		# Day 8
		self.assertEqual(result[7]['date'], '2023-04-08')
		self.assertAlmostEqual(result[7]['morning_capacity'], 0, delta=self.delta)
		self.assertAlmostEqual(result[7]['afternoon_capacity'], 0.27, delta=self.delta)

		# Day 9
		self.assertEqual(result[8]['date'], '2023-04-09')
		self.assertAlmostEqual(result[8]['morning_capacity'], 0.8, delta=self.delta)
		self.assertAlmostEqual(result[8]['afternoon_capacity'], 0.27, delta=self.delta)

		# Day 10
		self.assertEqual(result[9]['date'], '2023-04-10')
		self.assertAlmostEqual(result[9]['morning_capacity'], 0.6, delta=self.delta)
		self.assertAlmostEqual(result[9]['afternoon_capacity'], 0.45, delta=self.delta)


	def test_hour_value_error(self):
		start_date = datetime(2023, 4, 1, 9)
		end_date = datetime(2023, 4, 1, 18)
		work_intervals = [
			WorkInterval(datetime(2023, 4, 1, 9), datetime(2023, 4, 1, 18), 1),
		]
		with self.assertRaises(ValueError):

			tasks = [
				CapacityTask(datetime(2023, 4, 1, 1), datetime(2023, 4, 1, 24), 1),
			]


	def test_scenario_one_day_full_time_with_weird_inputs(self):

		start_date = datetime(2023, 4, 1, 9)
		end_date = datetime(2023, 4, 1, 18)
		work_intervals = [
			WorkInterval(datetime(2023, 4, 1, 9), datetime(2023, 4, 1, 18), 1),
		]

		tasks = [
			CapacityTask(datetime(2023, 4, 1, 10), datetime(2023, 4, 1, 12), 1),
			CapacityTask(datetime(2023, 4, 1, 14), datetime(2023, 4, 1, 16), 1),
			CapacityTask(datetime(2023, 4, 1, 17), datetime(2023, 4, 1, 18), 1),
			CapacityTask(datetime(2023, 4, 1, 9), datetime(2023, 4, 1, 10), 1),
			CapacityTask(datetime(2023, 4, 1, 12), datetime(2023, 4, 1, 14), 1),
			CapacityTask(datetime(2023, 4, 1, 16), datetime(2023, 4, 1, 17), 1),
			CapacityTask(datetime(2023, 4, 1, 9), datetime(2023, 4, 1, 18), 1),
			CapacityTask(datetime(2023, 4, 1, 8), datetime(2023, 4, 1, 18), 1),
			CapacityTask(datetime(2023, 4, 1, 8), datetime(2023, 4, 1, 19), 1),
			CapacityTask(datetime(2023, 4, 1, 8), datetime(2023, 4, 1, 20), 1),
			CapacityTask(datetime(2023, 4, 1, 0), datetime(2023, 4, 1, 23), 1),
		]

		params = CapacityCalculationParams(start_date, end_date, work_intervals, tasks)
		result = get_capacity_between_interval(params)
		self.assertEqual(len(result), 1)

		# Day 1
		self.assertEqual(result[0]['date'], '2023-04-01')
		self.assertAlmostEqual(result[0]['morning_capacity'], 1, delta=self.delta)
		self.assertAlmostEqual(result[0]['afternoon_capacity'], 1, delta=self.delta)