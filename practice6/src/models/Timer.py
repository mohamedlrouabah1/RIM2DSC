from time import perf_counter_ns
from enum import Enum


class TimeUnit(Enum):
    """
    Value to get the execution time in the desired unit
    given the per_counter_ns() function that return the
    time in nanoseconds.
    """
    NS = 1
    MS = 1_000_000
    S = 1_000_000_000
    MIN = 60_000_000_000
    HOUR = 3_600_000_000_000


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
        self.current = None

    def __len__(self) -> int:
        return len(self.measure)

    def __str__(self) -> str:
        print(f"Timer with {len(self)} measures")
        for name in self.measure:
            print(f" - {name} : {self.computation_time(name, self.default_unit)} {self.default_unit.name}")

    def start(self, name, force=False) -> bool:
        if self.current is not None:
            print("A timer is already started, stop it first.")
            return False

        if name in self.measure and not force:
            print("The name is already used, used force option to overwrite it.")
            return False

        self.measure[name] = [perf_counter_ns()]
        self.current = name
        pass

    def stop(self):
        if self.current is None:
            return False
        self.measure[self.current].append(perf_counter_ns())
        self.current = None
        return True

    def get_time(self, name) -> float:
        try:
            return self.format_time(name)
        except KeyError:
            return "Not measured"


    def __str__(self) -> str:
        timer_str = f"Timer with {len(self)} measures\n"
        for name in self.measure:
            timer_str += f" - {name} : {self.format_time(name)}\n"
        return timer_str

    def format_time(self, name) -> str:
        ns = self.measure[name][1] - self.measure[name][0]
        hours, remainder = divmod(ns, TimeUnit.HOUR.value)
        minutes, remainder = divmod(remainder, TimeUnit.MIN.value)
        seconds, remainder = divmod(remainder, TimeUnit.S.value)
        milliseconds, remainder = divmod(ns, TimeUnit.MS.value)
        formatted_time = f"{hours:02d}h{minutes:02d}m{seconds:02d}s{milliseconds:03d}ms{remainder:03d}ns (total: {ns}ns)"
        return formatted_time


    def display_histogram(self):
        raise NotImplementedError("Not implemented yet")
