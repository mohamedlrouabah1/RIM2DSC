import time
import unittest
from models.Timer import Timer, TimeUnit

class TestTimer(unittest.TestCase):

    def test_timer_init(self):
        # Test Timer initialization
        timer = Timer()
        self.assertIsNotNone(timer)
        self.assertEqual(len(timer), 0)

    def test_time_measurement(self):
        # Test time measurement using Timer
        timer = Timer()
        function_id = "test_function"
        sleep_time = 0.1  # in seconds

        # Measure the execution time of a function
        self.time_measure(timer, function_id, sleep_time)

        # Verify that the measurement has been added
        self.assertEqual(len(timer), 1)

        # Verify that the time is recorded in nanoseconds by default
        time_ns = timer.measure[function_id][1] - timer.measure[function_id][0]
        self.assertAlmostEqual(timer.get_time(function_id), time_ns, delta=1e6)

        # Verify that the time is correctly converted to milliseconds
        time_ms = time_ns / TimeUnit.MS.value
        timer.default_unit = TimeUnit.MS
        self.assertAlmostEqual(timer.get_time(function_id), time_ms, delta=1e-3)

        # Verify that the time is correctly converted to seconds
        time_s = time_ns / TimeUnit.S.value
        timer.default_unit = TimeUnit.S
        self.assertAlmostEqual(timer.get_time(function_id), time_s, delta=1e-3)

        # Verify that the time is correctly converted to minutes
        time_min = time_ns / TimeUnit.MIN.value
        timer.default_unit = TimeUnit.MIN
        self.assertAlmostEqual(timer.get_time(function_id), time_min, delta=1e-3)

        # Verify that the time is correctly converted to hours
        time_hour = time_ns / TimeUnit.HOUR.value
        timer.default_unit = TimeUnit.HOUR
        self.assertAlmostEqual(timer.get_time(function_id), time_hour, delta=1e-3)

    def time_measure(self, timer: Timer, function_id: str, sleep_time: float):
        # Helper method to measure time for testing
        timer.start(function_id)
        time.sleep(sleep_time)
        timer.stop()

if __name__ == "__main__":
    unittest.main()
