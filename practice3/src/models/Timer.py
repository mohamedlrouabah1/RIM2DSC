from time import perf_counter_ns
from enum import Enum
from Timer import TimeUnit

class Timer:
    """
    Used to store computed time in nanoseconds of the execution of a function.
    You can use the name (or an id) of the function to start and stop the timer
    for this function. 
    Then you can get the time in nanoseconds or in the desired unit using the
    TimeUnit enum.
    """

    def __init__(self, default_unit=TimeUnit.S):
        """
        Param:
            default_unit: TimeUnit
            The default unit to use when displaying the time of a function.
        """
        self.measure = {}
        self.default_unit = default_unit

    def __len__(self) -> int:
        return len(self.measure)

    def __str__(self) -> str:
        raise NotImplementedError("Not implemented yet")
        
    def start(self, name):
        self.measure[name] = [perf_counter_ns()]
        pass

    def stop(self, name):
        self.measure[name].append(perf_counter_ns())
        pass
    
    def computation_time(self, name, unit=TimeUnit.S) -> float:
        return (self.measure[name][1] - self.measure[name][0])/unit.value
        
    


class TimeUnit(Enum):
    """
    Value to get the execution time in the desired unit
    given the per_counter_ns() function that return the
    time in nanoseconds.
    """
    NS = 1
    MS = 1,000
    S = 1,000,000,000
    MIN = 60,000,000,000
    HOUR = 3,600,000,000,000