import time
import unittest

from models.Timer import Timer

class TestTimer(unittest.TestCase):


    def time_measure(self, timer:Timer, id:str, sleep_time:float):
        timer.start(id)
        time.sleep(sleep_time)
        timer.stop()


    def test_timer(self):
        timer = Timer()
        assert timer is not None
