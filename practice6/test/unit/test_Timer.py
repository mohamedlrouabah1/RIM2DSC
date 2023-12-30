from models.Timer import Timer
import time

def time_measure(timer:Timer, id:str, sleep_time:float):
    timer.start(id)
    time.sleep(sleep_time)
    timer.stop()


def test_timer():
    timer = Timer()
    assert timer is not None
