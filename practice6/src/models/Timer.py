from __future__ import annotations
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
    Timer class for measuring the execution time of functions and displaying results.

    Attributes:
    -----------
    - measure: dict
        A dictionary to store the start and stop times of measured functions.
    - default_unit: TimeUnit
        The default time unit to use when displaying the time.
    - current: str
        The name of the currently running timer.

    Methods:
    --------
    - __init__(self, default_unit=TimeUnit.S):
        Constructor for Timer.
    - __len__(self) -> int:
        Returns the number of measures recorded.
    - start(self, name, force=False) -> bool:
        Starts the timer for a function with the given name.
    - stop(self) -> bool:
        Stops the currently running timer.
    - get_time(self, name) -> float:
        Returns the formatted execution time for a function.
    - __str__(self) -> str:
        Returns a string representation of the Timer object.
    - format_time(self, name) -> str:
        Formats the execution time for a function.
    - display_histogram(self):
        Displays a histogram of the recorded execution times (not implemented).

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

    def start(self, name, force=False) -> bool:
        """
        Starts the timer for a function with the given name.

        Params:
        -------
        - name: str
            The name of the function.
        - force: bool
            If True, allows overwriting an existing timer with the same name.

        Returns:
        --------
        bool
            True if the timer is successfully started, False otherwise.

        """
        if self.current is not None:
            print("A timer is already started, stop it first.")
            return False

        if name in self.measure and not force:
            print("The name is already used, used force option to overwrite it.")
            return False

        self.measure[name] = [perf_counter_ns()]
        self.current = name

    def stop(self):
        """
        Stops the currently running timer.

        Returns:
        --------
        bool
            True if a timer was stopped, False otherwise.

        """
        if self.current is None:
            return False
        self.measure[self.current].append(perf_counter_ns())
        self.current = None
        return True

    def get_time(self, name) -> float:
        """
        Returns the formatted execution time for a function.

        Params:
        -------
        - name: str
            The name of the function.

        Returns:
        --------
        float
            The formatted execution time.

        """
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
        """
        Formats the execution time for a function.

        Params:
        -------
        - name: str
            The name of the function.

        Returns:
        --------
        str
            Formatted execution time.

        """
        ns = self.measure[name][1] - self.measure[name][0]
        hours, remainder = divmod(ns, TimeUnit.HOUR.value)
        minutes, remainder = divmod(remainder, TimeUnit.MIN.value)
        seconds, remainder = divmod(remainder, TimeUnit.S.value)
        milliseconds, remainder = divmod(ns, TimeUnit.MS.value)
        formatted_time = f"{hours:02d}h{minutes:02d}m{seconds:02d}s{milliseconds:03d}ms{remainder:03d}ns (total: {ns}ns)"
        return formatted_time


    def display_histogram(self):
        raise NotImplementedError("Not implemented yet")
