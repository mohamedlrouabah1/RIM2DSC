"""
NB: this file is depracated, it is not used anymore.
From now on see the class in models/Timer.py

"""

from datetime import timedelta



def convert_time_from_ns_to_s(t: float) -> float:
    """
    Convert time from nanoseconds to seconds

    Parameters:
    -----------
    t: float
        time in nanoseconds

    Returns:
    --------
    t: float
        time in seconds
    """
    return t / 1_000_000_000

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


# def print_time(t: float) -> None:
#     """
#         Print the time in the following format:
#         HH:MM:SS

#         Parameters:
#         -----------
#             t: float
#                 time in nanaseconds
#     """
#     t_in_ms = convert_time_from_ns_to_ms(t)
#     print("time (HH:MM:SS) ", end="")
#     print(timedelta(microseconds=t_in_ms, ))

def print_time(chartname: str, t: float) -> None:
    t_in_s = convert_time_from_ns_to_s(t)
    print(f"Time taken with {chartname} Indexing collection: {t_in_s:.2f} seconds")