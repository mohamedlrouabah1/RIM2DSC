from models import Timer, TimeUnit
import time

def test_time_measure(timer:Timer, id:str, sleep_time:float):
    timer.start(id)
    time.sleep(sleep_time)
    timer.stop()


def test_timer():
    timer = Timer()
    assert Timer() is not None
