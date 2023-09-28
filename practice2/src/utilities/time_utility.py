from datetime import timedelta


def convert_time_from_ns_to_ms(t: float) -> float:
    """
        Convert time from nanoseconds to milliseconds

        Parameters:
        -----------
            t: float
                time in nanaseconds

        Returns:
        --------
            t: float
                time in milliseconds
    """
    return t * 10**-3


def print_time(t: float) -> None:
    """
        Print the time in the following format:
        HH:MM:SS

        Parameters:
        -----------
            t: float
                time in nanaseconds
    """
    t_in_ms = convert_time_from_ns_to_ms(t)
    print("time (HH:MM:SS) ", end="")
    print(timedelta(microseconds=t_in_ms, ))
